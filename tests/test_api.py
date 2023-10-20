# -*- coding: utf-8 -*-

import pytest


def test():
    from awscli_mate import api

    _ = api.__version__
    _ = api.AWSCliConfig
    _ = api.SectionTypeEnum
    _ = api.ConfigKeyEnum
    _ = api.CredentialKeyEnum
    _ = api.get_account_alias
    _ = api.get_sign_in_url
    _ = api.get_switch_role_url

    awscli_config = api.AWSCliConfig()

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
