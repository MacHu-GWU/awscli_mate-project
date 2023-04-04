# -*- coding: utf-8 -*-

from awscli_mate.awscli import AWSCliConfig

awscli_config = AWSCliConfig()

awscli_config.mfa_auth(
    profile="your_profile",
    mfa_code="123456",
    overwrite_default=True,
)
