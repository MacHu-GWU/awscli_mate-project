# -*- coding: utf-8 -*-

import typing as T


def get_account_alias(iam_client) -> T.Optional[str]:
    import botocore.exceptions

    try:
        response = iam_client.list_account_aliases()
        return response["AccountAliases"][0]
    except botocore.exceptions.ClientError:
        return None
    except IndexError:
        return None
    except:
        raise


def get_sign_in_url(profile: str):
    """
    Get the url for signing in AWS console.

    See AWS official doc about sign in url at
    https://docs.aws.amazon.com/signin/latest/userguide/console-sign-in-tutorials.html
    """
    import boto3

    boto_ses = boto3.session.Session(profile_name=profile)
    iam = boto_ses.client("iam")
    account = get_account_alias(iam)
    if account is None:
        sts = boto_ses.client("sts")
        response = sts.get_caller_identity()
        account = response["Account"]
    return f"https://{account}.signin.aws.amazon.com/console/"


def get_switch_role_url(profile: str):
    """
    Get the url for switching role.

    See AWS official doc about switch role url at
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html

    In your ``${HOME}/.aws/config``, you need to have a ``my_acc_2_assumed_role_profile``
    like this::

        [profile my_acc_1_profile]
        region = us-east-1
        output = json

        [profile my_acc_2_assumed_role_profile]
        region = us-east-1
        role_arn = arn:aws:iam::111122223333:role/admin-role
        source_profile = my_acc_1_profile
    """
    import boto3

    boto_ses = boto3.session.Session(profile_name=profile)
    iam = boto_ses.client("iam")
    sts = boto_ses.client("sts")
    account = get_account_alias(iam)
    response = sts.get_caller_identity()
    if account is None:
        account = response["Account"]
    arn = response["Arn"]
    role_name = arn.split("/")[1]
    display_name = f"{role_name}@{account}"
    account = response["Account"]
    return f"https://signin.aws.amazon.com/switchrole?roleName={role_name}&account={account}&displayName={display_name}"
