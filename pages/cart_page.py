"""Корзина saucedemo — с шагами Allure."""
import allure
from selenium.webdriver.common.by import By

from config import settings
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = f"{settings.ui_url}/cart.html"

    ITEM_NAMES = (By.CSS_SELECTOR, ".cart_item [data-test='inventory-item-name']")
    CHECKOUT = (By.ID, "checkout")

    @allure.step("Получить список товаров в корзине")
    def item_names(self) -> list[str]:
        self.find(self.CHECKOUT)
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    @allure.step("Перейти к оформлению заказа")
    def checkout(self) -> None:
        self.click(self.CHECKOUT)
