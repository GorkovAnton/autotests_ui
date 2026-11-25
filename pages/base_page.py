"""Базовый PageObject: все ожидания живут здесь, страницы их только используют."""
from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]


class BasePage:
    URL = ""

    def __init__(self, driver: WebDriver, timeout: float = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.URL)
        return self

    def find(self, locator: Locator) -> WebElement:
        """Ждёт, пока элемент станет видимым, и возвращает его."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        """Ждёт появления хотя бы одного элемента и возвращает все."""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: Locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: Locator, text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text

    def is_visible(self, locator: Locator, timeout: float = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
