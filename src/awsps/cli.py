import sys

import click

from awsps import auth, cache, config, selector, sso


@click.group()
def main():
    """AWS Identity Center Permission Set CLI"""
    pass


@main.command()
@click.option("--start-url", default=None, help="AWS Identity Center 시작 URL")
@click.option("--region", default=None, help="AWS 리전")
def login(start_url, region):
    """로그인 후 Account/Permission Set을 선택하여 임시 자격증명을 출력합니다.

    사용법: eval $(awsps login)
    """
    cfg = config.load_config(start_url, region)

    # 토큰 캐시 확인
    access_token = cache.load_token(cfg.start_url)

    if not access_token:
        print("SSO 로그인을 시작합니다...", file=sys.stderr)
        access_token, expires_in = auth.login(cfg.start_url, cfg.region)
        cache.save_token(access_token, expires_in, cfg.start_url)
        print("로그인 성공!\n", file=sys.stderr)
    else:
        print("캐시된 토큰을 사용합니다.\n", file=sys.stderr)

    # Account 선택
    accounts = sso.list_accounts(access_token, cfg.region)
    account = selector.select_account(accounts)
    account_id = account["accountId"]
    account_name = account["accountName"]

    # Permission Set 선택
    roles = sso.list_account_roles(access_token, account_id, cfg.region)
    role = selector.select_role(roles, account_name)
    role_name = role["roleName"]

    print(f"\n{account_name} ({account_id}) / {role_name} 자격증명을 가져옵니다...",
          file=sys.stderr)

    # 자격증명 조회
    creds = sso.get_role_credentials(access_token, role_name, account_id, cfg.region)

    # stdout에 export문 출력
    print(f"export AWS_ACCESS_KEY_ID={creds['accessKeyId']}")
    print(f"export AWS_SECRET_ACCESS_KEY={creds['secretAccessKey']}")
    print(f"export AWS_SESSION_TOKEN={creds['sessionToken']}")

    print(f"\n자격증명이 설정되었습니다. (eval로 실행 시 자동 적용)", file=sys.stderr)


@main.command()
@click.option("--start-url", required=True, help="AWS Identity Center 시작 URL")
@click.option("--region", default="us-east-1", help="AWS 리전 (기본값: us-east-1)")
def configure(start_url, region):
    """AWS Identity Center 설정을 저장합니다."""
    config.save_config(start_url, region)
    click.echo(f"설정 저장 완료: {config.CONFIG_FILE}")
    click.echo(f"  start_url: {start_url}")
    click.echo(f"  region: {region}")
