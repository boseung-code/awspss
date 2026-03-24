import json
import os
from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path.home() / ".awsps"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    start_url: str
    region: str


def load_config(start_url: str | None = None, region: str | None = None) -> Config:
    file_config = _load_config_file()

    resolved_start_url = (
        start_url
        or os.environ.get("AWSPS_START_URL")
        or file_config.get("start_url")
    )
    resolved_region = (
        region
        or os.environ.get("AWSPS_REGION")
        or file_config.get("region")
        or "us-east-1"
    )

    if not resolved_start_url:
        raise click_missing_start_url()

    return Config(start_url=resolved_start_url, region=resolved_region)


def save_config(start_url: str, region: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {"start_url": start_url, "region": region}
    CONFIG_FILE.write_text(json.dumps(data, indent=2))


def _load_config_file() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def click_missing_start_url():
    import click
    return click.ClickException(
        "start-url이 필요합니다. --start-url 플래그, AWSPS_START_URL 환경변수, "
        "또는 'awsps configure'로 설정하세요."
    )
