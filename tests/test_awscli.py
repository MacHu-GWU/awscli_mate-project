# -*- coding: utf-8 -*-

import shutil
from pathlib import Path

import pytest

from awscli_mate.tests.paths import dir_tests
from awscli_mate.exc import ProfileNotFoundError
from awscli_mate.awscli import AWSCliConfig

dir_aws: Path = dir_tests.joinpath(".aws")
dir_aws_tmp: Path = dir_tests.joinpath(".aws_tmp")
path_aws_config: Path = dir_aws_tmp.joinpath("config")
path_aws_credentials: Path = dir_aws_tmp.joinpath("credentials")


class TestCliConfig:
    @classmethod
    def cleanup(cls):
        if dir_aws_tmp.exists():
            shutil.rmtree(str(dir_aws_tmp))

    @classmethod
    def setup_class(cls):
        cls.cleanup()
        shutil.copytree(str(dir_aws), str(dir_aws_tmp))

    @classmethod
    def teardown_class(cls):
        pass

    def test(self):
        awscli_config = AWSCliConfig(
            path_config=path_aws_config,
            path_credentials=path_aws_credentials,
        )
        config, credentials = awscli_config.read_config()

        awscli_config.ensure_profile_exists("default", config, credentials)
        awscli_config.ensure_profile_exists("p1", config, credentials)
        awscli_config.ensure_profile_exists("p2", config, credentials)
        awscli_config.ensure_profile_exists("p3", config, credentials)

        for profile in ["invalid", "profile p1"]:
            with pytest.raises(ProfileNotFoundError):
                awscli_config.ensure_profile_exists(profile, config, credentials)

        # ------------------------------------------------------------------------------
        # set_profile_as_default
        # ------------------------------------------------------------------------------
        for profile in ["p1", "p2", "p3"]:
            # before
            config, credentials = awscli_config.read_config()
            assert dict(config["default"]) != dict(config[f"profile {profile}"])
            assert dict(credentials["default"]) != dict(credentials[profile])

            # run
            awscli_config.set_profile_as_default(profile)

            # after
            config, credentials = awscli_config.read_config()
            assert dict(config["default"]) == dict(config[f"profile {profile}"])
            assert dict(credentials["default"]) == dict(credentials[profile])


if __name__ == "__main__":
    from awscli_mate.tests import run_cov_test

    run_cov_test(__file__, "awscli_mate.awscli", preview=False)
