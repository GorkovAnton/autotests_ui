"""UI: каталог и корзина."""
import allure
import pytest

from pages.cart_page import CartPage

pytestmark = [pytest.mark.ui, allure.epic("Saucedemo"), allure.feature("Корзина")]


@allure.story("Добавление товаров")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Бейдж корзины показывает количество товаров")
def test_cart_badge(inventory):
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.add_to_cart("Sauce Labs Bolt T-Shirt")

    assert inventory.cart_count() == 2


@allure.story("Добавление товаров")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("В корзине ровно добавленные товары")
def test_cart_contents(driver, inventory):
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.add_to_cart("Sauce Labs Bike Light")

    inventory.open_cart()

    assert CartPage(driver).item_names() == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]


@allure.story("Сортировка")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Сортировка по цене: {order}")
@pytest.mark.parametrize("order, reverse", [("lohi", False), ("hilo", True)])
def test_sort_by_price(inventory, order, reverse):
    inventory.sort_by(order)

    prices = inventory.product_prices()
    assert prices == sorted(prices, reverse=reverse)
