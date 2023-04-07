# -*- coding: utf-8 -*-

import pytest
import shutil
from pathlib_mate import Path
from awscli_mate.awscli import AWSCliConfig

dir_here = Path.dir_here(__file__)


def get_awscli_config(
    dir_tmp_path: Path,
    name: str,
) -> AWSCliConfig:
    dir_tmp_path = Path(dir_tmp_path)
    dir_tmp_path.remove_if_exists()
    dir_aws = dir_here.joinpath("home", name)
    shutil.copytree(dir_aws, dir_tmp_path)
    awscli_config = AWSCliConfig(
        path_config=dir_tmp_path.joinpath("config"),
        path_credentials=dir_tmp_path.joinpath("credentials"),
    )
    return awscli_config


@pytest.fixture
def awscli_config(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws")


@pytest.fixture
def awscli_config_empty(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws_empty")


@pytest.fixture
def awscli_config_no_config(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws_no_config")


@pytest.fixture
def awscli_config_no_credentials(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws_no_credentials")


@pytest.fixture
def awscli_config_bad_config(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws_bad_config")


@pytest.fixture
def awscli_config_bad_credentials(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws_bad_credentials")


@pytest.fixture
def awscli_config_profile_not_exist_in_config(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws_profile_not_exist_in_config")


@pytest.fixture
def awscli_config_profile_not_exist_in_credentials(tmp_path) -> AWSCliConfig:
    return get_awscli_config(tmp_path, ".aws_profile_not_exist_in_credentials")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
