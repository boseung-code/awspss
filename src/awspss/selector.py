import sys

from pzp import pzp
from pzp.exceptions import AbortAction, PZPException
from pzp.layout import (
    DefaultLayout, BOLD, CYAN, GREEN, RESET, BLACK_BG,
)


class ColorLayout(DefaultLayout, option="color"):
    def print_items(self, selected: int) -> None:
        for i, item in self.enumerate_items():
            is_selected = i + self.offset == selected
            self.screen.erase_line()
            if is_selected:
                self.screen.write(f"{GREEN}{BOLD}{self.config.pointer_str}").reset()
                self.screen.space(1).write(f"{GREEN}{BOLD}{self.config.format_fn(item)}").reset().nl()
            else:
                self.screen.write(f"{self.config.no_pointer_str}")
                self.screen.space(1).write(self.config.format_fn(item)).reset().nl()

    def print_header(self) -> None:
        if self.config.header_str:
            self.screen.erase_line().write(f"{CYAN}{BOLD}{self.config.header_str}").reset().nl()


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
            layout="color",
            pointer_str=">",
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
            layout="color",
            pointer_str=">",
        )
    except (AbortAction, PZPException, KeyboardInterrupt):
        selected = None

    if selected is None:
        print("Selection cancelled.", file=sys.stderr)
        raise SystemExit(1)

    return selected
