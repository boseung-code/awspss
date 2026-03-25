import json
import time
from datetime import datetime, timezone

import pytest

from awspss import cache


@pytest.fixture(autouse=True)
def tmp_cache(tmp_path, monkeypatch):
    cache_dir = tmp_path / "cache"
    monkeypatch.setattr(cache, "CACHE_DIR", cache_dir)
    monkeypatch.setattr(cache, "TOKEN_FILE", cache_dir / "token.json")
    monkeypatch.setattr(cache, "LAST_ACCOUNT_FILE", cache_dir / "last_account.json")
    return cache_dir


class TestTokenCache:
    def test_save_and_load(self):
        cache.save_token("test-token", 3600, "https://example.awsapps.com/start")
        token = cache.load_token("https://example.awsapps.com/start")
        assert token == "test-token"

    def test_load_returns_none_when_no_file(self):
        assert cache.load_token("https://example.awsapps.com/start") is None

    def test_load_returns_none_for_different_start_url(self):
        cache.save_token("test-token", 3600, "https://example.awsapps.com/start")
        assert cache.load_token("https://other.awsapps.com/start") is None

    def test_load_returns_none_when_expired(self):
        cache.save_token("test-token", 0, "https://example.awsapps.com/start")
        assert cache.load_token("https://example.awsapps.com/start") is None

    def test_load_returns_none_within_margin(self):
        # Token expires in 4 minutes (less than 5 min margin)
        cache.save_token("test-token", 240, "https://example.awsapps.com/start")
        assert cache.load_token("https://example.awsapps.com/start") is None

    def test_delete_token(self):
        cache.save_token("test-token", 3600, "https://example.awsapps.com/start")
        assert cache.delete_token() is True
        assert cache.load_token("https://example.awsapps.com/start") is None

    def test_delete_token_no_file(self):
        assert cache.delete_token() is False


class TestLastAccount:
    def test_save_and_load(self):
        cache.save_last_account("123456789012", "my-account")
        result = cache.load_last_account()
        assert result["accountId"] == "123456789012"
        assert result["accountName"] == "my-account"

    def test_load_returns_none_when_no_file(self):
        assert cache.load_last_account() is None
