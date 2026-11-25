"""Настройки фреймворка."""
import os
from dataclasses import dataclass, field


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


@dataclass(frozen=True)
class Settings:
    ui_url: str = field(default_factory=lambda: _env("UI_URL", "https://www.saucedemo.com").rstrip("/"))

    sauce_user: str = field(default_factory=lambda: _env("SAUCE_USER", "standard_user"))
    sauce_password: str = field(default_factory=lambda: _env("SAUCE_PASSWORD", "secret_sauce"))

    headless: bool = field(default_factory=lambda: _env("HEADLESS", "0") == "1")
    timeout: float = field(default_factory=lambda: float(_env("TIMEOUT", "10")))

settings = Settings()
