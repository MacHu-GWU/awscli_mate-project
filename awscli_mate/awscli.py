# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from pathlib import Path
from commentedconfigparser import CommentedConfigParser

from .paths import path_config, path_credentials
from .exc import ProfileNotFoundError


@dataclasses.dataclass
class AWSCliConfig:
    path_config: Path = dataclasses.field(default=path_config)
    path_credentials: Path = dataclasses.field(default=path_credentials)

    def read_config(self) -> T.Tuple[CommentedConfigParser, CommentedConfigParser]:
        config = CommentedConfigParser()
        config.read(self.path_config)
        credentials = CommentedConfigParser()
        credentials.read(self.path_credentials)
        return config, credentials

    def ensure_profile_exists(
        self,
        profile: str,
        config: CommentedConfigParser,
        credentials: CommentedConfigParser,
    ):
        msg = "Profile [{}] not found in {}"

        if profile != "default":
            section_name = f"profile {profile}"
        else:
            section_name = profile
        if section_name not in config:
            raise ProfileNotFoundError(msg.format(section_name, self.path_config))

        section_name = profile
        if section_name not in credentials:
            raise ProfileNotFoundError(msg.format(section_name, self.path_credentials))

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
    ):
        for k, v in list(config[from_section_name].items()):
            config[to_section_name][k] = v

    def replace_section_data(
        self,
        config: CommentedConfigParser,
        from_section_name: str,
        to_section_name: str,
    ) -> bool:
        """
        Replace section data, return a boolean flag to indicate that whether
        there is any data change.
        """
        if dict(config[from_section_name]) == dict(config[to_section_name]):
            return False

        self.clear_section_data(config, to_section_name)
        self.copy_section_data(config, from_section_name, to_section_name)
        return True

    def set_profile_as_default(self, profile: str):
        if profile == "default":
            return

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

    def mfa_auth(
        self,
        profile: str,
        mfa_code: str,
        hours: int = 12,
        overwrite_default: bool = False,
    ):  # pragma: no cover
        """
        Given a base ``${profile}``, do MFA authentication with ``mfa_code``,
        create / update the new aws profile ``${profile}_mfa`` using the returned
        temp token. This function will update the ``~/.aws/credential`` and
        ``~/.aws/config`` file inplace.

        :param aws_profile: The source AWS profile which has MFA enabled
        :param mfa_code: six digit MFA code
        :param hours: time-to-expire hours.
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

        response = sts.get_caller_identity()
        user_arn = response["Arn"]
        mfa_arn = user_arn.replace(":user/", ":mfa/", 1)

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

        # set initial value if section not exists
        if f"profile {new_profile}" not in config:
            config[f"profile {new_profile}"] = {}
        if new_profile not in credentials:
            credentials[new_profile] = {}

        flag_is_config_changed = self.replace_section_data(
            config,
            from_section_name=f"profile {profile}",
            to_section_name=f"profile {new_profile}",
        )

        self.clear_section_data(credentials, new_profile)
        credentials[new_profile]["aws_access_key_id"] = aws_access_key_id
        credentials[new_profile]["aws_secret_access_key"] = aws_secret_access_key
        credentials[new_profile]["aws_session_token"] = aws_session_token

        if overwrite_default:
            self.copy_section_data(config, f"profile {new_profile}", "default")
            self.copy_section_data(credentials, new_profile, "default")

        # update ~/.aws/config and ~/.aws/credentials file
        if flag_is_config_changed:
            with self.path_config.open("w") as f:
                config.write(f)

        with self.path_credentials.open("w") as f:
            credentials.write(f)
