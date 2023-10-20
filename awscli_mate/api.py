# -*- coding: utf-8 -*-

"""
Public API of awscli_mate.

Usage example::

    import awscli_mate.api as awscli_mate

    aws_cli_config = awscli_mate.AWSCliConfig()
    aws_cli_config.set_profile_as_default("my_profile")
"""

from ._version import __version__
from .awscli import strip_comment
from .awscli import AWSCliConfig
from .constants import SectionTypeEnum
from .constants import ConfigKeyEnum
from .constants import CredentialKeyEnum
from .url import get_account_alias
from .url import get_sign_in_url
from .url import get_switch_role_url
