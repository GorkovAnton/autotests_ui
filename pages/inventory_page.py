"""Каталог товаров saucedemo — с шагами Allure."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from config import settings
from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = f"{settings.ui_url}/inventory.html"

    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

    @staticmethod
    def _item_button(name: str, text: str):
        return (By.XPATH,
                f"//div[@data-test='inventory-item']"
                f"[.//div[@data-test='inventory-item-name' and normalize-space()='{name}']]"
                f"//button[normalize-space()='{text}']")

    @allure.step("Проверить, что открыт каталог")
    def is_opened(self) -> bool:
        return self.is_visible(self.TITLE) and self.text_of(self.TITLE) == "Products"

    def product_names(self) -> list[str]:
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def product_prices(self) -> list[float]:
        return [float(e.text.replace("$", "")) for e in self.find_all(self.ITEM_PRICES)]

    @allure.step("Добавить в корзину: {name}")
    def add_to_cart(self, name: str) -> None:
        self.click(self._item_button(name, "Add to cart"))

    @allure.step("Убрать из корзины: {name}")
    def remove_from_cart(self, name: str) -> None:
        self.click(self._item_button(name, "Remove"))

    @allure.step("Получить число на бейдже корзины")
    def cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    @allure.step("Отсортировать товары: {value}")
    def sort_by(self, value: str) -> None:
        Select(self.find(self.SORT)).select_by_value(value)

    @allure.step("Открыть корзину")
    def open_cart(self) -> None:
        self.click(self.CART_LINK)
