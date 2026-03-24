import sys

from pzp import pzp
from pzp.exceptions import AbortAction


def select_account(accounts: list[dict]) -> dict:
    if not accounts:
        print("접근 가능한 계정이 없습니다.", file=sys.stderr)
        raise SystemExit(1)

    try:
        selected = pzp(
            candidates=accounts,
            format_fn=lambda a: f"{a['accountName']} ({a['accountId']})",
            header_str="AWS Account를 선택하세요:",
            fullscreen=False,
            height=15,
        )
    except AbortAction:
        print("선택이 취소되었습니다.", file=sys.stderr)
        raise SystemExit(1)

    return selected


def select_role(roles: list[dict], account_name: str) -> dict:
    if not roles:
        print(f"{account_name}에 접근 가능한 Permission Set이 없습니다.", file=sys.stderr)
        raise SystemExit(1)

    if len(roles) == 1:
        role = roles[0]
        print(f"Permission Set 자동 선택: {role['roleName']}", file=sys.stderr)
        return role

    try:
        selected = pzp(
            candidates=roles,
            format_fn=lambda r: r["roleName"],
            header_str=f"[{account_name}] Permission Set을 선택하세요:",
            fullscreen=False,
            height=15,
        )
    except AbortAction:
        print("선택이 취소되었습니다.", file=sys.stderr)
        raise SystemExit(1)

    return selected
