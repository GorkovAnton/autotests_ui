"""Страница логина saucedemo — с шагами Allure."""
import allure
from selenium.webdriver.common.by import By

from config import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = f"{settings.ui_url}/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    @allure.step("Открыть страницу логина")
    def open(self):
        return super().open()

    @allure.step("Войти как {username}")
    def login(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    @allure.step("Прочитать сообщение об ошибке")
    def error_message(self) -> str:
        return self.text_of(self.ERROR)
