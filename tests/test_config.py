import pytest

from gateway.config import Settings


def test_config_with_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("UPSTREAM_URL", raising=False)
    settings = Settings(_env_file=None)
    assert settings.upstream_url == "http://localhost:9000"


def test_config_with_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("UPSTREAM_URL", "http://example.test:1234")
    settings = Settings(_env_file=None)
    assert settings.upstream_url == "http://example.test:1234"
