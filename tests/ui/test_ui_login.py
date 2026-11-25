"""UI: авторизация на saucedemo."""
import allure
import pytest

from config import settings
from pages.login_page import LoginPage

pytestmark = [pytest.mark.ui, allure.epic("Saucedemo"), allure.feature("Авторизация")]


@pytest.mark.smoke
@allure.story("Логин")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Успешный логин открывает каталог")
def test_login_success(driver, inventory):
    assert driver.current_url.endswith("/inventory.html")


@allure.story("Логин")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Заблокированный пользователь видит ошибку")
def test_locked_out_user(driver):
    page = LoginPage(driver).open()

    page.login("locked_out_user", settings.sauce_password)

    assert "Sorry, this user has been locked out" in page.error_message()


@allure.story("Логин")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Пользователь видит ошибку при вводе невалидных username = {username}")
@pytest.mark.parametrize("username", ["INVALID_USERNAME", "blablabla"])
def test_login_invalid(driver, username):
    page = LoginPage(driver).open()
    page.login(username, settings.sauce_password)

    assert "Epic sadface: Username and password do not match any user in this service" in page.error_message()