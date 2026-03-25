import json
import os
from pathlib import Path

import pytest

from awspss import config


@pytest.fixture(autouse=True)
def tmp_config(tmp_path, monkeypatch):
    config_dir = tmp_path / ".awspss"
    config_file = config_dir / "config.json"
    monkeypatch.setattr(config, "CONFIG_DIR", config_dir)
    monkeypatch.setattr(config, "CONFIG_FILE", config_file)
    monkeypatch.delenv("AWSPSS_START_URL", raising=False)
    monkeypatch.delenv("AWSPSS_REGION", raising=False)
    return config_file


class TestSaveConfig:
    def test_creates_file(self, tmp_config):
        config.save_config("https://example.awsapps.com/start", "us-west-2")
        data = json.loads(tmp_config.read_text())
        assert data["start_url"] == "https://example.awsapps.com/start"
        assert data["region"] == "us-west-2"

    def test_overwrites_existing(self, tmp_config):
        config.save_config("https://old.awsapps.com/start", "us-east-1")
        config.save_config("https://new.awsapps.com/start", "ap-northeast-2")
        data = json.loads(tmp_config.read_text())
        assert data["start_url"] == "https://new.awsapps.com/start"


class TestLoadConfig:
    def test_from_file(self, tmp_config):
        config.save_config("https://example.awsapps.com/start", "us-west-2")
        cfg = config.load_config()
        assert cfg.start_url == "https://example.awsapps.com/start"
        assert cfg.region == "us-west-2"

    def test_cli_flags_override_file(self, tmp_config):
        config.save_config("https://file.awsapps.com/start", "us-east-1")
        cfg = config.load_config(start_url="https://cli.awsapps.com/start", region="eu-west-1")
        assert cfg.start_url == "https://cli.awsapps.com/start"
        assert cfg.region == "eu-west-1"

    def test_env_vars_override_file(self, tmp_config, monkeypatch):
        config.save_config("https://file.awsapps.com/start", "us-east-1")
        monkeypatch.setenv("AWSPSS_START_URL", "https://env.awsapps.com/start")
        monkeypatch.setenv("AWSPSS_REGION", "ap-southeast-1")
        cfg = config.load_config()
        assert cfg.start_url == "https://env.awsapps.com/start"
        assert cfg.region == "ap-southeast-1"

    def test_cli_flags_override_env(self, tmp_config, monkeypatch):
        monkeypatch.setenv("AWSPSS_START_URL", "https://env.awsapps.com/start")
        cfg = config.load_config(start_url="https://cli.awsapps.com/start")
        assert cfg.start_url == "https://cli.awsapps.com/start"

    def test_default_region(self, tmp_config):
        config.save_config("https://example.awsapps.com/start", "us-west-2")
        # Manually write config without region
        tmp_config.parent.mkdir(parents=True, exist_ok=True)
        tmp_config.write_text(json.dumps({"start_url": "https://example.awsapps.com/start"}))
        cfg = config.load_config()
        assert cfg.region == "us-east-1"

    def test_missing_start_url_raises(self, tmp_config):
        with pytest.raises(Exception):
            config.load_config()
