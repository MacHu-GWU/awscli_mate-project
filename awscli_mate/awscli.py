# -*- coding: utf-8 -*-

"""
This module provides a set of functions to interact with AWS CLI.
"""

import typing as T
import dataclasses
from pathlib import Path
import configparser

from pathlib_mate import Path as PathlibMatePath
from commentedconfigparser import CommentedConfigParser

from .paths import path_config, path_credentials
from . import exc


def strip_comment(s: str) -> str:
    return s.split("#")[0]


T_PROFILE_REGION_PAIR = T.Tuple[str, str]


@dataclasses.dataclass
class AWSCliConfig:
    """
    Abstraction of the AWS CLI config files.
    """

    path_config: Path = dataclasses.field(default=path_config)
    path_credentials: Path = dataclasses.field(default=path_credentials)

    def read_config(
        self,
    ) -> T.Tuple[CommentedConfigParser, CommentedConfigParser]:
        """
        parse ~/.aws/config and ~/.aws/credentials file, return two config objects.
        """
        if not self.path_config.exists():
            raise exc.AWSConfigFileNotExistError(f"{self.path_config} not exist!")
        if not self.path_credentials.exists():
            raise exc.AWSCredentialsFileNotExistError(
                f"{self.path_credentials} not exist!"
            )

        try:
            config = CommentedConfigParser()
            config.read(self.path_config)
        except configparser.ParsingError as e:
            raise exc.MalformedConfigFileError(str(e))

        try:
            credentials = CommentedConfigParser()
            credentials.read(self.path_credentials)
        except configparser.ParsingError as e:
            raise exc.MalformedConfigFileError(str(e))

        return config, credentials

    def extract_profile_and_region_pairs(self) -> T.List[T_PROFILE_REGION_PAIR]:
        """
        Extract profile and region pairs from the config file, except the
        default profile.

        .. note::

            note that the credentials file is not used here, config file
            should be your top priority.

        :return: a list of (profile, region) pairs
        """
        config, _ = self.read_config()
        pairs = list()
        for section_name, section in config.items():
            # extract the profile name
            # we don't want the configparser's DEFAULT section
            # and also we don't want to use the default profile as the base profile
            if not section_name.startswith("profile "):
                continue
            profile = section_name[8:]
            # extract the region name
            region = section.get("region", "unknown-region")
            pairs.append((profile, region))
        return pairs

    def ensure_profile_exists(
        self,
        profile: str,
        config: CommentedConfigParser,
        credentials: CommentedConfigParser,
    ):
        """
        Ensure the profile exists in the config and credentials object.
        """
        msg = "Profile [{}] not found in {}"

        if profile != "default":
            section_name = f"profile {profile}"
        else:
            section_name = profile
        if section_name not in config:
            raise exc.ProfileNotFoundError(msg.format(section_name, self.path_config))

        section_name = profile
        if section_name not in credentials:
            raise exc.ProfileNotFoundError(
                msg.format(section_name, self.path_credentials)
            )

    def clear_section_data(
        self,
        config: CommentedConfigParser,
        section_name: str,
    ) -> bool:
        """
        Clear section data, return a boolean flag to indicate that whether
        there is any data change.
        """
        kv_list = list(config[section_name].items())
        for k, v in kv_list:
            config[section_name].pop(k)
        return len(kv_list) > 0

    def copy_section_data(
        self,
        config: CommentedConfigParser,
        from_section_name: str,
        to_section_name: str,
        create_if_not_exist: bool = False,
    ):
        """
        Copy section data from one profile to another.
        """
        if create_if_not_exist:
            if to_section_name not in config:
                config[to_section_name] = {}
        for k, v in list(config[from_section_name].items()):
            config[to_section_name][k] = v

    def replace_section_data(
        self,
        config: CommentedConfigParser,
        from_section_name: str,
        to_section_name: str,
        create_if_not_exist: bool = False,
    ) -> bool:
        """
        Replace section data, return a boolean flag to indicate that whether
        there is any data change.
        """
        if create_if_not_exist:
            if to_section_name not in config:
                config[to_section_name] = {
                    "this_is_a_dummy_key": "this_is_a_dummy_value"
                }

        if dict(config[from_section_name]) == dict(config[to_section_name]):
            return False

        self.clear_section_data(config, to_section_name)
        self.copy_section_data(config, from_section_name, to_section_name)
        return True

    def set_profile_as_default(
        self,
        profile: str,
    ) -> T.Tuple[T.Optional[CommentedConfigParser], T.Optional[CommentedConfigParser]]:
        """
        Set the given profile as the default profile by replacing the section data.
        """
        if profile == "default":
            return None, None

        config, credentials = self.read_config()

        self.ensure_profile_exists("default", config, credentials)
        self.ensure_profile_exists(profile, config, credentials)

        flag_is_config_changed = self.replace_section_data(
            config,
            from_section_name=f"profile {profile}",
            to_section_name="default",
        )
        flag_is_credentials_changed = self.replace_section_data(
            credentials,
            from_section_name=profile,
            to_section_name="default",
        )

        if flag_is_config_changed:
            with self.path_config.open("w") as f:
                config.write(f)

        if flag_is_credentials_changed:
            with self.path_credentials.open("w") as f:
                credentials.write(f)

        return config, credentials

    def mfa_auth(
        self,
        profile: str,
        mfa_code: str,
        hours: int = 12,
        overwrite_default: bool = False,
        mfa_arn: T.Optional[str] = None,
    ) -> T.Tuple[CommentedConfigParser, CommentedConfigParser]:  # pragma: no cover
        """
        Given a base ``${profile}``, do MFA authentication with ``mfa_code``,
        create / update the new aws profile ``${profile}_mfa`` using the returned
        temp token. This function will update the ``~/.aws/credential`` and
        ``~/.aws/config`` file inplace.

        :param aws_profile: The source AWS profile which has MFA enabled
        :param mfa_code: six digit MFA code
        :param hours: time-to-expire hours.
        :param overwrite_default: whether to overwrite the default awscli profile
        :param mfa_arn: MFA arn, if not provided, it will assume the MFA arn
            is arn:aws:iam::{account_id}:mfa/{user_name}
        """
        # validate input
        if profile == "default":
            msg = "you cannot use the default profile for MFA authentication!"
            raise ValueError(msg)

        if (mfa_code.isdigit() is False) or (len(mfa_code) != 6):
            msg = "mfa_code must be a six digit number"
            raise ValueError(msg)

        # get MFA authentication session token
        import boto3

        boto_ses = boto3.session.Session(profile_name=profile)
        sts = boto_ses.client("sts")

        if mfa_arn is None:
            response = sts.get_caller_identity()
            account_id = response["Account"]
            user_arn = response["Arn"]
            user_name = user_arn.split("/")[-1]
            mfa_arn = f"arn:aws:iam::{account_id}:mfa/{user_name}"

        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.get_session_token
        response = sts.get_session_token(
            SerialNumber=mfa_arn,
            TokenCode=mfa_code,
            DurationSeconds=hours * 3600,
        )

        aws_access_key_id = response["Credentials"]["AccessKeyId"]
        aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
        aws_session_token = response["Credentials"]["SessionToken"]

        # read existing config / credentials data
        config, credentials = self.read_config()

        # update config / credentials data in memory
        new_profile = "{}_mfa".format(profile)

        # update config data
        # set initial value if section not exists
        if f"profile {new_profile}" not in config:
            flag_is_config_changed = True
            self.copy_section_data(
                config,
                from_section_name=f"profile {profile}",
                to_section_name=f"profile {new_profile}",
            )
        else:
            flag_is_config_changed = False

        # because mfa_auth is for the credentials
        # we respect the ``..._mfa`` profile if it already exists,
        # and it is different from te base profile
        # we don't do ``replace_section_data`` here

        # update credential data
        # set initial value if section not exists
        if new_profile not in credentials:
            credentials[new_profile] = {}
        self.clear_section_data(credentials, new_profile)
        credentials[new_profile]["aws_access_key_id"] = aws_access_key_id
        credentials[new_profile]["aws_secret_access_key"] = aws_secret_access_key
        credentials[new_profile]["aws_session_token"] = aws_session_token

        if overwrite_default:
            self.copy_section_data(config, f"profile {new_profile}", "default")
            self.copy_section_data(credentials, new_profile, "default")

        # update ~/.aws/config and ~/.aws/credentials file
        if flag_is_config_changed:
            with PathlibMatePath(self.path_config).atomic_open("w", overwrite=True) as f:
                config.write(f)

        with PathlibMatePath(self.path_credentials).atomic_open("w", overwrite=True) as f:
            credentials.write(f)

        return config, credentials
