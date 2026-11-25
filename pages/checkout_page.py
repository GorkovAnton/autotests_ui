"""Оформление заказа saucedemo — с шагами Allure."""
import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")
    ITEM_TOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    FINISH = (By.ID, "finish")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    @allure.step("Заполнить данные покупателя: {first_name} {last_name}, {postal_code}")
    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)

    @allure.step("Нажать Continue")
    def submit_info(self) -> None:
        self.click(self.CONTINUE)

    @allure.step("Прочитать сообщение об ошибке")
    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    @allure.step("Получить сумму товаров")
    def item_total(self) -> float:
        return float(self.text_of(self.ITEM_TOTAL).split("$")[1])

    @allure.step("Нажать Finish")
    def finish(self) -> None:
        self.click(self.FINISH)

    @allure.step("Прочитать заголовок завершения")
    def complete_header(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)
