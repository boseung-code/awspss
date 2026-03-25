import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

CACHE_DIR = Path.home() / ".awspss" / "cache"
TOKEN_FILE = CACHE_DIR / "token.json"

EXPIRY_MARGIN_SECONDS = 300  # 5분 여유


def load_token(start_url: str) -> str | None:
    if not TOKEN_FILE.exists():
        return None

    try:
        data = json.loads(TOKEN_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None

    if data.get("startUrl") != start_url:
        return None

    expires_at = data.get("expiresAt")
    if not expires_at:
        return None

    expiry_time = datetime.fromisoformat(expires_at).timestamp()
    if time.time() >= expiry_time - EXPIRY_MARGIN_SECONDS:
        return None

    return data.get("accessToken")


def save_token(access_token: str, expires_in: int, start_url: str) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    expires_at = datetime.fromtimestamp(
        time.time() + expires_in, tz=timezone.utc
    ).isoformat()

    data = {
        "accessToken": access_token,
        "expiresAt": expires_at,
        "startUrl": start_url,
    }

    TOKEN_FILE.write_text(json.dumps(data, indent=2))
    os.chmod(TOKEN_FILE, 0o600)


def delete_token() -> bool:
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        return True
    return False


LAST_ACCOUNT_FILE = CACHE_DIR / "last_account.json"


def save_last_account(account_id: str, account_name: str) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    data = {"accountId": account_id, "accountName": account_name}
    LAST_ACCOUNT_FILE.write_text(json.dumps(data, indent=2))


def load_last_account() -> dict | None:
    if not LAST_ACCOUNT_FILE.exists():
        return None
    try:
        return json.loads(LAST_ACCOUNT_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None
