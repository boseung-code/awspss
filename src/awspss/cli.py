import os
import sys
from pathlib import Path

import click

from awspss import auth, cache, config, selector, sso

SHELL_FUNCTION = """\
awspss() {
  case "$1" in
    login|sw|unset)
      local _out
      _out="$(command awspss "$@")"
      local _rc=$?
      if [ $_rc -eq 0 ]; then
        eval "$_out"
      else
        echo "$_out" >&2
      fi
      return $_rc
      ;;
    *)
      command awspss "$@"
      ;;
  esac
}
"""

INIT_LINE = 'eval "$(awspss init --print)"'


def _get_rc_file() -> Path:
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return Path.home() / ".zshrc"
    return Path.home() / ".bashrc"


def _is_already_registered(rc_file: Path) -> bool:
    if not rc_file.exists():
        return False
    return "awspss init" in rc_file.read_text()


@click.group()
def main():
    """AWS Identity Center Permission Sets Switcher"""
    pass


@main.command()
@click.option("--print", "print_only", is_flag=True, help="Print shell function only")
def init(print_only):
    """Register shell function"""
    if print_only:
        print(SHELL_FUNCTION)
        return

    rc_file = _get_rc_file()

    if _is_already_registered(rc_file):
        click.echo(f"Already registered in {rc_file}.", err=True)
    elif click.confirm(f"Register shell function to {rc_file}?", default=True, err=True):
        with open(rc_file, "a") as f:
            f.write(f"\n# awspss - AWS Identity Center Permission Sets Switcher\n{INIT_LINE}\n")
        click.echo(f"Registered to {rc_file}.", err=True)
    else:
        click.echo("Cancelled.", err=True)
        click.echo(f"To add manually: {INIT_LINE}", err=True)
        return

    if not sys.stdout.isatty():
        print(SHELL_FUNCTION)


def _get_token(cfg: config.Config) -> str:
    access_token = cache.load_token(cfg.start_url)
    if not access_token:
        print("Starting SSO login...", file=sys.stderr)
        access_token, expires_in = auth.login(cfg.start_url, cfg.region)
        cache.save_token(access_token, expires_in, cfg.start_url)
        print("Login successful.\n", file=sys.stderr)
    else:
        print("Using cached token.\n", file=sys.stderr)
    return access_token


def _select_and_print_credentials(access_token: str, cfg: config.Config):
    accounts = sso.list_accounts(access_token, cfg.region)
    account = selector.select_account(accounts)
    account_id = account["accountId"]
    account_name = account["accountName"]

    roles = sso.list_account_roles(access_token, account_id, cfg.region)
    role = selector.select_role(roles, account_name)
    role_name = role["roleName"]

    print(f"\nFetching credentials for {account_name} ({account_id}) / {role_name}...",
          file=sys.stderr)

    creds = sso.get_role_credentials(access_token, role_name, account_id, cfg.region)

    print(f"export AWS_ACCESS_KEY_ID={creds['accessKeyId']}")
    print(f"export AWS_SECRET_ACCESS_KEY={creds['secretAccessKey']}")
    print(f"export AWS_SESSION_TOKEN={creds['sessionToken']}")

    print(f"\nCredentials set.", file=sys.stderr)


@main.command()
@click.option("--start-url", default=None, help="SSO start URL")
@click.option("--region", default=None, help="AWS region")
def login(start_url, region):
    """SSO login"""
    cfg = config.load_config(start_url, region)

    print("Starting SSO login...", file=sys.stderr)
    access_token, expires_in = auth.login(cfg.start_url, cfg.region)
    cache.save_token(access_token, expires_in, cfg.start_url)
    print("Login successful.\n", file=sys.stderr)

    _select_and_print_credentials(access_token, cfg)


@main.command()
@click.option("--start-url", default=None, help="SSO start URL")
@click.option("--region", default=None, help="AWS region")
def sw(start_url, region):
    """Switch account/permission set"""
    cfg = config.load_config(start_url, region)
    access_token = _get_token(cfg)
    _select_and_print_credentials(access_token, cfg)


@main.command()
def unset():
    """Clear AWS credentials from current shell"""
    print("unset AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN")
    print("Credentials cleared.", file=sys.stderr)


@main.command()
@click.option("--start-url", default=None, help="SSO start URL")
@click.option("--region", default=None, help="AWS region")
def configure(start_url, region):
    """Configure SSO connection"""
    if not start_url:
        start_url = click.prompt("AWS Identity Center start URL", type=str)
    if not region:
        region = click.prompt("AWS region", default="us-east-1", type=str)

    config.save_config(start_url, region)
    click.echo(f"\nConfiguration saved: {config.CONFIG_FILE}")
    click.echo(f"  start_url: {start_url}")
    click.echo(f"  region: {region}")
