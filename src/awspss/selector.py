import sys

from pzp import pzp
from pzp.exceptions import AbortAction, PZPException


def select_account(accounts: list[dict]) -> dict:
    if not accounts:
        print("No accessible accounts found.", file=sys.stderr)
        raise SystemExit(1)

    try:
        selected = pzp(
            candidates=accounts,
            format_fn=lambda a: f"{a['accountName']} ({a['accountId']})",
            header_str="Select AWS Account:",
            fullscreen=False,
            height=15,
        )
    except (AbortAction, PZPException, KeyboardInterrupt):
        selected = None

    if selected is None:
        print("Selection cancelled.", file=sys.stderr)
        raise SystemExit(1)

    return selected


def select_role(roles: list[dict], account_name: str) -> dict:
    if not roles:
        print(f"No permission sets found for {account_name}.", file=sys.stderr)
        raise SystemExit(1)

    if len(roles) == 1:
        role = roles[0]
        print(f"Auto-selected: {role['roleName']}", file=sys.stderr)
        return role

    try:
        selected = pzp(
            candidates=roles,
            format_fn=lambda r: r["roleName"],
            header_str=f"[{account_name}] Select Permission Set:",
            fullscreen=False,
            height=15,
        )
    except (AbortAction, PZPException, KeyboardInterrupt):
        selected = None

    if selected is None:
        print("Selection cancelled.", file=sys.stderr)
        raise SystemExit(1)

    return selected
