# -*- coding: utf-8 -*-

"""
A simple CLI tool to help you to do MFA authentication with AWS CLI.

Usage:

.. code-block:: bash

    python mfa_auth.py --base_profile your_profile --mfa_token 123456
"""

import fire
from awscli_mate.awscli import AWSCliConfig

awscli_config = AWSCliConfig()


def mfa_auth(
    base_profile: str,
    mfa_token: str,
):
    awscli_config.mfa_auth(
        profile=base_profile,
        mfa_code=str(mfa_token),
        overwrite_default=True,
    )


if __name__ == "__main__":
    fire.Fire(mfa_auth)
