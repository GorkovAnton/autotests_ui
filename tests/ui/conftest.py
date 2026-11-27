"""Фикстуры UI-тестов."""
import pytest
from selenium import webdriver

from config import settings
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def chrome_options(headless: bool) -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-features=PasswordLeakDetection")
    return options


@pytest.fixture
def driver(request):
    headless = settings.headless or request.config.getoption("--headless")
    drv = webdriver.Chrome(options=chrome_options(headless))
    yield drv
    drv.quit()


@pytest.fixture
def inventory(driver) -> InventoryPage:
    LoginPage(driver).open().login(settings.sauce_user, settings.sauce_password)
    page = InventoryPage(driver)
    assert page.is_opened(), "после логина не открылся каталог"
    return page
