# -*- coding: utf-8 -*-

"""
Public API of awscli_mate
"""

from .awscli import (
    strip_comment,
    AWSCliConfig,
)
from .constants import (
    SectionTypeEnum,
    ConfigKeyEnum,
    CredentialKeyEnum,
)
