# -*- coding: utf-8 -*-

import pytest

from awscli_mate.exc import ProfileNotFoundError
from awscli_mate.awscli import AWSCliConfig


class TestCliConfig:
    def test(self, awscli_config: AWSCliConfig):
        config, credentials = awscli_config.read_config()

        awscli_config.ensure_profile_exists("default", config, credentials)
        awscli_config.ensure_profile_exists("p1", config, credentials)
        awscli_config.ensure_profile_exists("p2", config, credentials)
        awscli_config.ensure_profile_exists("p3", config, credentials)

        for profile in ["invalid", "profile p1"]:
            with pytest.raises(ProfileNotFoundError):
                awscli_config.ensure_profile_exists(profile, config, credentials)

        pairs = awscli_config.extract_profile_and_region_pairs()
        assert len(pairs) == 3

        # ------------------------------------------------------------------------------
        # copy section data
        # ------------------------------------------------------------------------------
        awscli_config.copy_section_data(
            config,
            from_section_name="profile p3",
            to_section_name="profile p4",
            create_if_not_exist=True,
        )
        assert "profile p4" in config

        # ------------------------------------------------------------------------------
        # replace section data
        # ------------------------------------------------------------------------------
        awscli_config.replace_section_data(
            config,
            from_section_name="profile p3",
            to_section_name="profile p5",
            create_if_not_exist=True,
        )
        assert "profile p5" in config

        assert (
            awscli_config.replace_section_data(
                config,
                from_section_name="profile p3",
                to_section_name="profile p5",
                create_if_not_exist=True,
            )
            is False
        )

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

        awscli_config.set_profile_as_default("default")


if __name__ == "__main__":
    from awscli_mate.tests import run_cov_test

    run_cov_test(__file__, "awscli_mate.awscli", preview=False)
