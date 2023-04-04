# -*- coding: utf-8 -*-

import os
from awscli_mate.tests.paths import dir_tests
from awscli_mate.config_parser import Config


class TestConfig:
    def test(self):
        config_file = dir_tests.joinpath("test.ini")
        dump_config_file = dir_tests.joinpath("dump-test.ini")
        config = Config.from_file(config_file)

        config.put("bob", "email", "bob@gmail.com")
        config.put("bob", "pwd", "bobpassword")
        config.put("bob", "title", "SDE")

        config.put("profile alice", "email", "bob@gmail.com")
        config.put("profile alice", "pwd", "bobpwd")
        config.put("profile alice", "title", "HR")

        config.put("default", "name", "cathy")
        config.put("default", "email", "cathy@email.com")

        config.dump(dump_config_file)

        new_config = Config.from_file(dump_config_file)
        assert new_config._data == {
            "default": {"name": "cathy", "email": "cathy@email.com"},
            "profile alice": {
                "name": "alice",
                "email": "bob@gmail.com",
                "pwd": "bobpwd",
                "title": "HR",
            },
            "bob": {
                "name": "bob",
                "email": "bob@gmail.com",
                "pwd": "bobpassword",
                "title": "SDE",
            },
        }


if __name__ == "__main__":
    from awscli_mate.tests import run_cov_test

    run_cov_test(__file__, "awscli_mate.config_parser", preview=False)
