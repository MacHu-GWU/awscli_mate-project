# -*- coding: utf-8 -*-

import fire
from .awscli import AWSCliConfig


class Cli:
    def set_profile_as_default(self, profile: str):
        """
        Set an named profile as default.
        """
        AWSCliConfig().set_profile_as_default(
            profile=profile,
        )

    def mfa_auth(
        self,
        profile: str,
        mfa_code: str,
        hours: int = 12,
        overwrite_default: bool = False,
    ):
        """
        Do MFA authentication.
        """
        AWSCliConfig().mfa_auth(
            profile=profile,
            mfa_code=str(mfa_code),
            hours=hours,
            overwrite_default=overwrite_default,
        )


def main():
    fire.Fire(Cli)
