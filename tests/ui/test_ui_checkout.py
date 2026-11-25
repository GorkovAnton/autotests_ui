"""UI: оформление заказа."""
import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

pytestmark = [pytest.mark.ui, allure.epic("Saucedemo"), allure.feature("Оформление заказа")]


@pytest.mark.smoke
@allure.story("Полный сценарий")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Покупка двух товаров от каталога до подтверждения")
def test_full_checkout(driver, inventory):
    inventory.add_to_cart("Sauce Labs Backpack")
    inventory.add_to_cart("Sauce Labs Bike Light")
    inventory.open_cart()
    CartPage(driver).checkout()
    checkout = CheckoutPage(driver)

    checkout.fill_info("Антон", "Горьков", "101000")
    checkout.submit_info()

    assert checkout.item_total() == pytest.approx(29.99 + 9.99)
    checkout.finish()
    assert checkout.complete_header() == "Thank you for your order!"


@allure.story("Валидация")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Без имени покупателя заказ не оформить")
def test_first_name_required(driver, inventory):
    inventory.add_to_cart("Sauce Labs Onesie")
    inventory.open_cart()
    CartPage(driver).checkout()
    checkout = CheckoutPage(driver)

    checkout.submit_info()

    assert checkout.error_message() == "Error: First Name is required"
