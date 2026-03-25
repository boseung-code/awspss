import boto3


def list_accounts(access_token: str, region: str) -> list[dict]:
    sso = boto3.client("sso", region_name=region)
    accounts = []
    paginator = sso.get_paginator("list_accounts")
    for page in paginator.paginate(accessToken=access_token):
        accounts.extend(page["accountList"])
    accounts.sort(key=lambda a: a["accountName"].lower())
    return accounts


def list_account_roles(access_token: str, account_id: str, region: str) -> list[dict]:
    sso = boto3.client("sso", region_name=region)
    roles = []
    paginator = sso.get_paginator("list_account_roles")
    for page in paginator.paginate(accessToken=access_token, accountId=account_id):
        roles.extend(page["roleList"])
    roles.sort(key=lambda r: r["roleName"].lower())
    return roles


def get_role_credentials(
    access_token: str, role_name: str, account_id: str, region: str
) -> dict:
    sso = boto3.client("sso", region_name=region)
    response = sso.get_role_credentials(
        roleName=role_name,
        accountId=account_id,
        accessToken=access_token,
    )
    return response["roleCredentials"]
