import sys

import click

from awsps import auth, cache, config, selector, sso

SHELL_FUNCTION = """\
awsps() {
  case "$1" in
    login|sw)
      local _out
      _out="$(command awsps _"$1" "${@:2}")"
      local _rc=$?
      if [ $_rc -eq 0 ]; then
        eval "$_out"
      else
        echo "$_out" >&2
      fi
      return $_rc
      ;;
    *)
      command awsps "$@"
      ;;
  esac
}
"""


@click.group()
def main():
    """AWS Identity Center Permission Set CLI"""
    pass


@main.command()
def init():
    """Shell 함수를 출력합니다. .bashrc/.zshrc에 eval "$(awsps init)"을 추가하세요."""
    print(SHELL_FUNCTION)


def _get_token(cfg: config.Config) -> str:
    access_token = cache.load_token(cfg.start_url)
    if not access_token:
        print("SSO 로그인을 시작합니다...", file=sys.stderr)
        access_token, expires_in = auth.login(cfg.start_url, cfg.region)
        cache.save_token(access_token, expires_in, cfg.start_url)
        print("로그인 성공!\n", file=sys.stderr)
    else:
        print("캐시된 토큰을 사용합니다.\n", file=sys.stderr)
    return access_token


def _select_and_print_credentials(access_token: str, cfg: config.Config):
    accounts = sso.list_accounts(access_token, cfg.region)
    account = selector.select_account(accounts)
    account_id = account["accountId"]
    account_name = account["accountName"]

    roles = sso.list_account_roles(access_token, account_id, cfg.region)
    role = selector.select_role(roles, account_name)
    role_name = role["roleName"]

    print(f"\n{account_name} ({account_id}) / {role_name} 자격증명을 가져옵니다...",
          file=sys.stderr)

    creds = sso.get_role_credentials(access_token, role_name, account_id, cfg.region)

    print(f"export AWS_ACCESS_KEY_ID={creds['accessKeyId']}")
    print(f"export AWS_SECRET_ACCESS_KEY={creds['secretAccessKey']}")
    print(f"export AWS_SESSION_TOKEN={creds['sessionToken']}")

    print(f"\n자격증명이 설정되었습니다.", file=sys.stderr)


@main.command(name="_login")
@click.option("--start-url", default=None, help="AWS Identity Center 시작 URL")
@click.option("--region", default=None, help="AWS 리전")
def login_internal(start_url, region):
    """SSO 로그인 후 Account/Permission Set을 선택하여 자격증명을 출력합니다."""
    cfg = config.load_config(start_url, region)
    access_token = _get_token(cfg)
    _select_and_print_credentials(access_token, cfg)


@main.command(name="_sw")
@click.option("--start-url", default=None, help="AWS Identity Center 시작 URL")
@click.option("--region", default=None, help="AWS 리전")
def switch_internal(start_url, region):
    """Account/Permission Set을 재선택하여 자격증명을 전환합니다."""
    cfg = config.load_config(start_url, region)
    access_token = cache.load_token(cfg.start_url)

    if not access_token:
        print("캐시된 토큰이 없습니다. 먼저 awsps login을 실행하세요.", file=sys.stderr)
        raise SystemExit(1)

    _select_and_print_credentials(access_token, cfg)


@main.command()
@click.option("--start-url", required=True, help="AWS Identity Center 시작 URL")
@click.option("--region", default="us-east-1", help="AWS 리전 (기본값: us-east-1)")
def configure(start_url, region):
    """AWS Identity Center 설정을 저장합니다."""
    config.save_config(start_url, region)
    click.echo(f"설정 저장 완료: {config.CONFIG_FILE}")
    click.echo(f"  start_url: {start_url}")
    click.echo(f"  region: {region}")
