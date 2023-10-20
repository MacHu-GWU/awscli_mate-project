# -*- coding: utf-8 -*-

import typing as T
import subprocess
import dataclasses

import fire
import zelfred.api as zf

from .vendor.better_fuzzywuzzy import FuzzyMatcher
from .vendor.os_platform import IS_WINDOWS
from .awscli import AWSCliConfig
from .url import get_sign_in_url, get_switch_role_url


@dataclasses.dataclass
class SetProfileItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
        awscli_config = AWSCliConfig()
        awscli_config.set_profile_as_default(profile=self.arg)
        print(f"set {self.arg!r} as the default profile.")


class SetProfileItemFuzzyMatcher(FuzzyMatcher[SetProfileItem]):
    def get_name(self, item: SetProfileItem) -> T.Optional[str]:
        return " ".join(item.arg.split("_"))


@dataclasses.dataclass
class MfaAuthItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
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


@dataclasses.dataclass
class MfaHintItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
        url = "https://repost.aws/knowledge-center/authenticate-mfa-cli"
        if IS_WINDOWS:
            subprocess.run(["start", url])
        else:
            subprocess.run(["open", url])


class MfaAuthItemFuzzyMatcher(FuzzyMatcher[MfaAuthItem]):
    def get_name(self, item: MfaAuthItem) -> T.Optional[str]:
        return " ".join(item.arg.split("_"))


@dataclasses.dataclass
class SignInProfileItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
        url = get_sign_in_url(profile=self.arg)
        zf.open_url(url)
        print(f"open {url} in default browser.")


class SignInProfileItemFuzzyMatcher(FuzzyMatcher[SignInProfileItem]):
    def get_name(self, item: SignInProfileItem) -> T.Optional[str]:
        return " ".join(item.arg.split("_"))


@dataclasses.dataclass
class SwitchRoleProfileItem(zf.Item):
    def enter_handler(self, ui: zf.UI):
        url = get_switch_role_url(profile=self.arg)
        zf.open_url(url)
        print(f"open {url} in default browser.")


class SwitchRoleItemFuzzyMatcher(FuzzyMatcher[SwitchRoleProfileItem]):
    def get_name(self, item: SwitchRoleProfileItem) -> T.Optional[str]:
        return " ".join(item.arg.split("_"))


class MenuEnum:
    set_profile_as_default = "set_profile_as_default"
    mfa_auth = "mfa_auth"
    sign_in = "sign_in"
    switch_role = "switch_role"


def show_top_menu(query: str, ui: zf.UI):
    return [
        SetProfileItem(
            title="📝 Set an named profile as default",
            subtitle="Hit 'Tab' to search profile",
            uid="uid-1",
            autocomplete=f"{MenuEnum.set_profile_as_default} ",
        ),
        SetProfileItem(
            title="🔐 Do CLI MFA Authentication",
            subtitle="Hit 'Tab' to select a base profile",
            uid="uid-2",
            autocomplete=f"{MenuEnum.mfa_auth} ",
        ),
        SetProfileItem(
            title="🌐 Sign in to AWS Console",
            subtitle="Hit 'Tab' to select a profile to sign in",
            uid="uid-3",
            autocomplete=f"{MenuEnum.sign_in} ",
        ),
        SetProfileItem(
            title="🔄 Switch Role in to AWS Console",
            subtitle="Hit 'Tab' to select a profile to switch to",
            uid="uid-4",
            autocomplete=f"{MenuEnum.switch_role} ",
        ),
    ]


def extract_profile_and_region_pairs() -> T.List[T.Tuple[str, str]]:
    awscli_config = AWSCliConfig()
    config, credentials = awscli_config.read_config()
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


def set_profile_as_default_handler(query: str, ui: zf.UI):
    q = zf.Query.from_str(query)
    pairs = extract_profile_and_region_pairs()
    items = [
        SetProfileItem(
            title=f"📝 {profile} | {region}",
            subtitle=f"Hit 'Enter' to set {profile!r} as the default profile.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.set_profile_as_default} {profile}",
        )
        for profile, region in pairs
    ]
    # example:
    # - ""
    # - "    "
    if len(q.trimmed_parts) == 0:
        return items
    else:
        matcher = SetProfileItemFuzzyMatcher.from_items(items)
        return matcher.match(" ".join(q.trimmed_parts), threshold=0, limit=99)


def _list_profile() -> T.List[MfaAuthItem]:
    return [
        MfaAuthItem(
            title=f"🔐 {profile} | {region}",
            subtitle=f"Hit 'Tab' to use this base profile for MFA auth.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.mfa_auth} {profile} ",
        )
        for profile, region in extract_profile_and_region_pairs()
    ]


def _select_profile(
    query: str,
    items: T.List[MfaAuthItem],
) -> T.List[MfaAuthItem]:
    """
    :param query: the query string. example: "my_profile_name"
    """
    matcher = MfaAuthItemFuzzyMatcher.from_items(items)
    return matcher.match(query, threshold=0, limit=99)


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
    ui: zf.UI,
) -> T.List[T.Union[MfaAuthItem, MfaHintItem]]:
    """

    :param query: the query string. example: "my_profile_name my_mfa_token"
    """
    q = zf.Query.from_str(query)
    # example:
    # - ""
    # - "    "
    if len(q.trimmed_parts) == 0:
        return _list_profile()
    elif q.trimmed_parts[0].startswith("?"):
        # sf.items.append(get_help_item())
        return []
    # example:
    # - "profile_name"
    # - "profile_substr"
    elif len(q.trimmed_parts) == 1:
        items = _list_profile()
        profiles = [item.arg for item in items]
        if q.trimmed_parts[0] in profiles:
            return _ask_for_mfa_token(profile=q.trimmed_parts[0])
        else:
            return _select_profile(query=" ".join(q.trimmed_parts), items=items)
    elif len(q.trimmed_parts) == 2:
        profile, token = q.trimmed_parts
        items = _list_profile()
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
            return _select_profile(query=" ".join(q.trimmed_parts), items=items)
    # example:
    # - "profile sub str"
    # - "profile sub str 123456"
    elif len(q.trimmed_parts) >= 3:
        items = _list_profile()
        profiles = [item.arg for item in items]
        profile = q.trimmed_parts[0]
        if profile in profiles:
            return _entered_invalid_token(profile, token=" ".join(q.trimmed_parts[1:]))
        else:
            return _select_profile(query=" ".join(q.trimmed_parts), items=items)
    else:  # pragma: no cover
        raise NotImplementedError


def sign_in_handler(
    query: str,
    ui: zf.UI,
) -> T.List[SignInProfileItem]:
    """ """
    q = zf.Query.from_str(query)
    pairs = extract_profile_and_region_pairs()
    items = [
        SignInProfileItem(
            title=f"📝 {profile} | {region}",
            subtitle=f"Hit 'Enter' to sign in using {profile!r} profile.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.sign_in} {profile}",
        )
        for profile, region in pairs
    ]
    # example:
    # - ""
    # - "    "
    if len(q.trimmed_parts) == 0:
        return items
    else:
        matcher = SignInProfileItemFuzzyMatcher.from_items(items)
        return matcher.match(" ".join(q.trimmed_parts), threshold=0, limit=99)


def switch_role_handler(
    query: str,
    ui: zf.UI,
) -> T.List[SwitchRoleProfileItem]:
    """ """
    q = zf.Query.from_str(query)
    pairs = extract_profile_and_region_pairs()
    items = [
        SwitchRoleProfileItem(
            title=f"📝 {profile} | {region}",
            subtitle=f"Hit 'Enter' to switch to IAM role defined in {profile!r}.",
            uid=profile,
            arg=profile,
            autocomplete=f"{MenuEnum.switch_role} {profile}",
        )
        for profile, region in pairs
    ]
    # example:
    # - ""
    # - "    "
    if len(q.trimmed_parts) == 0:
        return items
    else:
        matcher = SwitchRoleItemFuzzyMatcher.from_items(items)
        return matcher.match(" ".join(q.trimmed_parts), threshold=0, limit=99)


handler_mapper = {
    MenuEnum.set_profile_as_default: set_profile_as_default_handler,
    MenuEnum.mfa_auth: mfa_auth_handler,
    MenuEnum.sign_in: sign_in_handler,
    MenuEnum.switch_role: switch_role_handler,
}


def handler(query: str, ui: zf.UI):
    parts = query.split(" ", 1)
    if len(parts) == 1:
        return show_top_menu(query, ui)
    handler_name = parts[0]
    handler_query = parts[1]
    return handler_mapper[handler_name](handler_query, ui)


def run_ui():
    zf.debugger.reset()
    zf.debugger.enable()
    ui = zf.UI(handler=handler, capture_error=False)
    ui.run()


def main():
    fire.Fire(run_ui)
