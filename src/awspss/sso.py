import sys

import boto3
from botocore.exceptions import ClientError, BotoCoreError


def _handle_error(e: Exception, action: str) -> None:
    if isinstance(e, ClientError):
        code = e.response["Error"]["Code"]
        if code == "UnauthorizedException" or code == "ForbiddenException":
            print(f"Error: Token expired or invalid. Please run 'awspss login'.", file=sys.stderr)
        else:
            print(f"Error: {action} failed - {e.response['Error']['Message']}", file=sys.stderr)
    elif isinstance(e, BotoCoreError):
        print(f"Error: {action} failed - {e}", file=sys.stderr)
    else:
        print(f"Error: {action} failed - {e}", file=sys.stderr)
    raise SystemExit(1)


def list_accounts(access_token: str, region: str) -> list[dict]:
    try:
        sso = boto3.client("sso", region_name=region)
        accounts = []
        paginator = sso.get_paginator("list_accounts")
        for page in paginator.paginate(accessToken=access_token):
            accounts.extend(page["accountList"])
        accounts.sort(key=lambda a: a["accountName"].lower())
        return accounts
    except (ClientError, BotoCoreError) as e:
        _handle_error(e, "List accounts")


def list_account_roles(access_token: str, account_id: str, region: str) -> list[dict]:
    try:
        sso = boto3.client("sso", region_name=region)
        roles = []
        paginator = sso.get_paginator("list_account_roles")
        for page in paginator.paginate(accessToken=access_token, accountId=account_id):
            roles.extend(page["roleList"])
        roles.sort(key=lambda r: r["roleName"].lower())
        return roles
    except (ClientError, BotoCoreError) as e:
        _handle_error(e, "List roles")


def get_role_credentials(
    access_token: str, role_name: str, account_id: str, region: str
) -> dict:
    try:
        sso = boto3.client("sso", region_name=region)
        response = sso.get_role_credentials(
            roleName=role_name,
            accountId=account_id,
            accessToken=access_token,
        )
        return response["roleCredentials"]
    except (ClientError, BotoCoreError) as e:
        _handle_error(e, "Get credentials")
