# -*- coding: utf-8 -*-

import enum


class SectionTypeEnum(str, enum.Enum):
    profile = "profile"
    sso_session = "sso-session"


class ConfigKeyEnum(str, enum.Enum):
    region = "region"
    output = "output"
    role_arn = "role_arn"
    source_profile = "source_profile"
    sso_session = "sso_session"
    sso_account_id = "sso_account_id"
    sso_role_name = "sso_role_name"
    sso_region = "sso_region"
    sso_start_url = "sso_start_url"


class CredentialKeyEnum(str, enum.Enum):
    aws_access_key_id = "aws_access_key_id"
    aws_secret_access_key = "aws_secret_access_key"
    aws_session_token = "aws_session_token"
