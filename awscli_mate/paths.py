# -*- coding: utf-8 -*-

from pathlib import Path

dir_home = Path.home()

# See "Location of the shared config and credentials files": https://docs.aws.amazon.com/sdkref/latest/guide/file-location.html
dir_aws = dir_home / ".aws"
path_config = dir_aws / "config"
path_credentials = dir_aws / "credentials"
