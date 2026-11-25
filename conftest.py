"""Корневой conftest: опции командной строки, хуки и окружение для Allure."""
import os
import platform
from pathlib import Path

import allure
import pytest

from config import settings


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="запускать браузер без окна")


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    """Скриншот, HTML и URL страницы в Allure при падении UI-теста."""
    report = yield
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            allure.attach(driver.get_screenshot_as_png(), name="Скриншот при падении",
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(driver.page_source, name="HTML страницы", attachment_type=allure.attachment_type.HTML)
            allure.attach(driver.current_url, name="URL", attachment_type=allure.attachment_type.URI_LIST)
    return report


@pytest.fixture(scope="session", autouse=True)
def allure_environment(request):
    yield
    alluredir = request.config.getoption("--alluredir", default=None)
    if not alluredir:
        return
    Path(alluredir).mkdir(parents=True, exist_ok=True)
    env = {
        "UI_URL": settings.ui_url,
        "Python": platform.python_version(),
        "OS": f"{platform.system()} {platform.release()}",
        "Headless": str(settings.headless or request.config.getoption("--headless")),
        "CI": os.getenv("CI", "false"),
    }
    (Path(alluredir) / "environment.properties").write_text(
        "\n".join(f"{k}={v}" for k, v in env.items()), encoding="utf-8")
