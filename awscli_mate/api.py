# -*- coding: utf-8 -*-

"""
Public API of awscli_mate
"""

from .awscli import strip_comment
from .awscli import AWSCliConfig
from .constants import SectionTypeEnum
from .constants import ConfigKeyEnum
from .constants import CredentialKeyEnum
from .url import get_account_alias
from .url import get_sign_in_url
from .url import get_switch_role_url
