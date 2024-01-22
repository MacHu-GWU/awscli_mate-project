# -*- coding: utf-8 -*-

import typing as T
import subprocess
import dataclasses

import fire
import zelfred.api as zf
from .vendor.os_platform import IS_WINDOWS

from .awscli import AWSCliConfig
from .search import get_sorted_profile_region_pairs
from .url import get_sign_in_url, get_switch_role_url


class UI(zf.UI):
    def format_highlight(self, s: str) -> str:
        return f"{self.terminal.cyan}{s}{self.terminal.normal}"

    def format_shortcut(self, s: str) -> str:
        return f"{self.terminal.magenta}{s}{self.terminal.normal}"

    @property
    def Tab(self) -> str:
        return self.format_shortcut("Tab")

    @property
    def Enter(self) -> str:
        return self.format_shortcut("Enter")


def display_profile_info(profile: str):
    print(f"try to get detailed info about the profile: {profile!r} ...")
    try:
        import boto3
        import botocore.exceptions

        boto_ses = boto3.session.Session(profile_name=profile)

        try:
            res = boto_ses.client("sts").get_caller_identity()
            aws_account_id = res["Account"]
            print(f"AWS Account ID = {aws_account_id}")
        except botocore.exceptions.ClientError:
            pass

        try:
            res = boto_ses.client("iam").list_account_aliases()
            aliases = res.get("AccountAliases", [])
            if aliases:
                print(f"AWS Account Alias = {aliases[0]}")
        except botocore.exceptions.ClientError:
            pass

        try:
            print(f"AWS Region = {boto_ses.region_name}")
        except:
            pass

    except ImportError:
        print("  you don't have boto3 installed.")


@dataclasses.dataclass
class ProfileItem(zf.Item):
    @classmethod
    def from_profile_region(cls, ui: UI, profile: str, region: str):
        raise NotImplementedError

    @classmethod
    def from_query(cls, ui: UI, query: str):
        sorted_pairs = get_sorted_profile_region_pairs(query)
        return [
            cls.from_profile_region(ui, profile, region)
            for profile, region in sorted_pairs
        ]


@dataclasses.dataclass
class SetProfileItem(ProfileItem):
    def enter_handler(self, ui: UI):
        awscli_config = AWSCliConfig()
        awscli_config.set_profile_as_default(profile=self.arg)
        print(f"set {self.arg!r} as the default profile.")
        display_profile_info(profile=self.arg)

    @classmethod
    def from_profile_region(cls, ui: UI, profile: str, region: str):
        "{term.cyan}{text}{term.normal}"
        return cls(
            title=f"📝 {ui.format_highlight(profile)} | {region}",
            subtitle=f"Hit '{ui.Enter}' to set {profile!r} as the default profile.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.set_profile_as_default} {profile}",
        )


@dataclasses.dataclass
class MfaAuthItem(ProfileItem):
    def enter_handler(self, ui: UI):
        awscli_config = AWSCliConfig()
        if not self.variables:
            return
        profile = self.variables["profile"]
        token = self.variables["token"]
        awscli_config.mfa_auth(
            profile=profile,
            mfa_code=token,
            overwrite_default=True,
        )
        print(
            f"aws cli MFA with: base profile = {profile!r}, new profile = '{profile}_mfa'"
        )
        display_profile_info(profile=f"{profile}_mfa")

    @classmethod
    def from_profile_region(cls, ui: UI, profile: str, region: str):
        return cls(
            title=f"🔐 {ui.format_highlight(profile)} | {region}",
            subtitle=f"Hit '{ui.Tab}' to use this base profile for MFA auth.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.mfa_auth} {profile} ",
        )


@dataclasses.dataclass
class MfaHintItem(zf.Item):
    def enter_handler(self, ui: UI):
        url = "https://repost.aws/knowledge-center/authenticate-mfa-cli"
        if IS_WINDOWS:
            subprocess.run(["start", url])
        else:
            subprocess.run(["open", url])


@dataclasses.dataclass
class SignInProfileItem(ProfileItem):
    def enter_handler(self, ui: UI):
        url = get_sign_in_url(profile=self.arg)
        zf.open_url(url)
        print(f"open {url} in default browser.")

    @classmethod
    def from_profile_region(cls, ui: UI, profile: str, region: str):
        return cls(
            title=f"📝 {ui.format_highlight(profile)} | {region}",
            subtitle=f"Hit '{ui.Enter}' to sign in using {profile!r} profile.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.sign_in} {profile}",
        )


@dataclasses.dataclass
class SwitchRoleProfileItem(ProfileItem):
    def enter_handler(self, ui: UI):
        url = get_switch_role_url(profile=self.arg)
        zf.open_url(url)
        print(f"open {url} in default browser.")

    @classmethod
    def from_profile_region(cls, ui: UI, profile: str, region: str):
        return cls(
            title=f"📝 {ui.format_highlight(profile)} | {region}",
            subtitle=f"Hit '{ui.Enter}' to switch to IAM role defined in {profile!r}.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.switch_role} {profile}",
        )


class MenuEnum:
    set_profile_as_default = "set_profile_as_default"
    mfa_auth = "mfa_auth"
    sign_in = "sign_in"
    switch_role = "switch_role"


def show_top_menu(query: str, ui: UI):
    return [
        SetProfileItem(
            title="📝 Set an named profile as default",
            subtitle=f"Hit '{ui.Tab}' to search profile",
            uid="uid-1",
            autocomplete=f"{MenuEnum.set_profile_as_default} ",
        ),
        SetProfileItem(
            title="🔐 Do CLI MFA Authentication",
            subtitle=f"Hit '{ui.Tab}' to select a base profile",
            uid="uid-2",
            autocomplete=f"{MenuEnum.mfa_auth} ",
        ),
        SetProfileItem(
            title="🌐 Sign in to AWS Console",
            subtitle=f"Hit '{ui.Tab}' to select a profile to sign in",
            uid="uid-3",
            autocomplete=f"{MenuEnum.sign_in} ",
        ),
        SetProfileItem(
            title="🔄 Switch Role in to AWS Console",
            subtitle=f"Hit '{ui.Tab}' to select a profile to switch to",
            uid="uid-4",
            autocomplete=f"{MenuEnum.switch_role} ",
        ),
    ]


def set_profile_as_default_handler(query: str, ui: UI):
    q = zf.Query.from_str(query)
    sorted_pairs = get_sorted_profile_region_pairs(query=" ".join(q.trimmed_parts))
    # example:
    # - ""
    # - "    "
    return [
        SetProfileItem.from_profile_region(ui, profile, region)
        for profile, region in sorted_pairs
    ]


def _ask_for_mfa_token(
    profile: str,
) -> T.List[MfaHintItem]:
    """
    :param profile: the selected profile name.
    """
    return [
        MfaHintItem(
            title=f"🔐 MFA with {profile!r}, enter your six digit MFA token ...",
            subtitle="Hit 'Enter' to read the official doc",
            uid="uid",
        )
    ]


def _entering_mfa_token(
    profile: str,
    token: str,
) -> T.List[MfaAuthItem]:
    return [
        MfaAuthItem(
            title=f"🔐 MFA with {profile!r} + {token!r} ...",
            subtitle="Continue to enter your six digit MFA token ...",
            uid="uid",
        )
    ]


def _entered_invalid_token(
    profile: str,
    token: str,
):
    return [
        MfaAuthItem(
            title=f"🔐 {token!r} is NOT a valid six digit MFA token!",
            subtitle="Hit 'Tab' to re-enter your six digit MFA token",
            uid="uid",
            autocomplete=f"{MenuEnum.mfa_auth} {profile} ",
        )
    ]


def _run_mfa_auth(
    profile: str,
    token: str,
):
    return [
        MfaAuthItem(
            title=f"🔐 MFA with {profile!r} + {token!r} ...",
            subtitle="Hit 'Enter' to do MFA authentication ...",
            uid="uid",
            variables={
                "profile": profile,
                "token": token,
            },
        )
    ]


def mfa_auth_handler(
    query: str,
    ui: UI,
) -> T.List[T.Union[MfaAuthItem, MfaHintItem]]:
    """

    :param query: the query string. example: "my_profile_name my_mfa_token"
    """
    q = zf.Query.from_str(query)
    # example:
    # - ""
    # - "    "
    if len(q.trimmed_parts) == 0:
        return MfaAuthItem.from_query(ui=ui, query="")
    elif q.trimmed_parts[0].startswith("?"):
        # sf.items.append(get_help_item())
        return []
    # example:
    # - "profile_name"
    # - "profile_substr"
    elif len(q.trimmed_parts) == 1:
        items = MfaAuthItem.from_query(ui=ui, query="")
        profiles = [item.arg for item in items]
        if q.trimmed_parts[0] in profiles:
            return _ask_for_mfa_token(profile=q.trimmed_parts[0])
        else:
            return MfaAuthItem.from_query(ui=ui, query=" ".join(q.trimmed_parts))
    elif len(q.trimmed_parts) == 2:
        profile, token = q.trimmed_parts
        items = MfaAuthItem.from_query(ui=ui, query="")
        profiles = [item.arg for item in items]
        # see below
        if profile in profiles:
            # see below
            if token.isdigit():
                # - "profile 123"
                if len(token) < 6:
                    return _entering_mfa_token(profile, token)
                # - "profile 123456"
                elif len(token) == 6:
                    return _run_mfa_auth(profile, token)
                # - "profile 123456789"
                elif len(token) >= 6:
                    return _entered_invalid_token(profile, token)
                else:  # pragma: no cover
                    raise NotImplementedError
            # - "profile abc"
            else:
                return _entered_invalid_token(profile, token)
        # - "alice bob"
        else:
            return MfaAuthItem.from_query(ui=ui, query=" ".join(q.trimmed_parts))
    # example:
    # - "profile sub str"
    # - "profile sub str 123456"
    elif len(q.trimmed_parts) >= 3:
        items = MfaAuthItem.from_query(ui=ui, query="")
        profiles = [item.arg for item in items]
        profile = q.trimmed_parts[0]
        if profile in profiles:
            return _entered_invalid_token(profile, token=" ".join(q.trimmed_parts[1:]))
        else:
            return MfaAuthItem.from_query(ui=ui, query=" ".join(q.trimmed_parts))
    else:  # pragma: no cover
        raise NotImplementedError


def sign_in_handler(
    query: str,
    ui: UI,
) -> T.List[SignInProfileItem]:
    """ """
    q = zf.Query.from_str(query)
    # example:
    # - ""
    # - "    "
    return SignInProfileItem.from_query(ui=ui, query=" ".join(q.trimmed_parts))


def switch_role_handler(
    query: str,
    ui: UI,
) -> T.List[SwitchRoleProfileItem]:
    """ """
    q = zf.Query.from_str(query)
    # example:
    # - ""
    # - "    "
    return SwitchRoleProfileItem.from_query(ui=ui, query=" ".join(q.trimmed_parts))


handler_mapper = {
    MenuEnum.set_profile_as_default: set_profile_as_default_handler,
    MenuEnum.mfa_auth: mfa_auth_handler,
    MenuEnum.sign_in: sign_in_handler,
    MenuEnum.switch_role: switch_role_handler,
}


def handler(query: str, ui: UI):
    parts = query.split(" ", 1)
    if len(parts) == 1:
        return show_top_menu(query, ui)
    handler_name = parts[0]
    handler_query = parts[1]
    return handler_mapper[handler_name](handler_query, ui)


def run_ui():
    zf.debugger.reset()
    zf.debugger.enable()
    ui = UI(handler=handler, capture_error=False)
    ui.run()


def main():
    fire.Fire(run_ui)
