# -*- coding: utf-8 -*-

import pytest


def test():
    import awscli_mate

    _ = awscli_mate.AWSCliConfig
    _ = awscli_mate.SectionTypeEnum
    _ = awscli_mate.ConfigKeyEnum
    _ = awscli_mate.CredentialKeyEnum

    awscli_config = awscli_mate.AWSCliConfig()

    _ = awscli_config.set_profile_as_default
    _ = awscli_config.mfa_auth

    _ = awscli_config.read_config
    _ = awscli_config.ensure_profile_exists
    _ = awscli_config.clear_section_data
    _ = awscli_config.copy_section_data
    _ = awscli_config.replace_section_data



if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
