# -*- coding: utf-8 -*-
import pytest
from pathlib_mate import Path
from awscli_mate.awscli import AWSCliConfig
from awscli_mate import exc

def test_awscli_config_empty(
    awscli_config_empty: AWSCliConfig,
):
    with pytest.raises(exc.AWSConfigFileNotExistError):
        awscli_config_empty.set_profile_as_default("p1")

def test_awscli_config_no_config(
    awscli_config_no_config: AWSCliConfig,
):
    with pytest.raises(exc.AWSConfigFileNotExistError):
        awscli_config_no_config.set_profile_as_default("p1")


def test_awscli_config_no_credentials(
    awscli_config_no_credentials: AWSCliConfig,
):
    with pytest.raises(exc.AWSCredentialsFileNotExistError):
        awscli_config_no_credentials.set_profile_as_default("p1")


def test_awscli_config_bad_config(
    awscli_config_bad_config: AWSCliConfig,
):
    with pytest.raises(exc.MalformedConfigFileError):
        awscli_config_bad_config.set_profile_as_default("p1")


def test_awscli_config_bad_credentials(
    awscli_config_bad_credentials: AWSCliConfig,
):
    with pytest.raises(exc.MalformedConfigFileError):
        awscli_config_bad_credentials.set_profile_as_default("p1")


def test_awscli_config_profile_not_exist_in_config(
    awscli_config_profile_not_exist_in_config: AWSCliConfig,
):
    with pytest.raises(exc.ProfileNotFoundError):
        awscli_config_profile_not_exist_in_config.set_profile_as_default("p1")


def test_awscli_config_profile_not_exist_in_credentials(
    awscli_config_profile_not_exist_in_credentials: AWSCliConfig,
):
    with pytest.raises(exc.ProfileNotFoundError):
        awscli_config_profile_not_exist_in_credentials.set_profile_as_default("p1")



if __name__ == "__main__":
    from awscli_mate.tests import run_cov_test

    run_cov_test(__file__, "awscli_mate.awscli", preview=False)
