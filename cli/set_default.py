# -*- coding: utf-8 -*-

"""
A simple CLI tool to help you to set named AWS profile as default

Usage:

.. code-block:: bash

    python set_default.py --profile your_profile
"""

import fire
from awscli_mate.awscli import AWSCliConfig

awscli_config = AWSCliConfig()


def set_default(
    profile: str,
):
    awscli_config.set_profile_as_default(profile)


if __name__ == "__main__":
    fire.Fire(set_default)
