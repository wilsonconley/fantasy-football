from __future__ import annotations

import contextlib
import typing as t

import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


@contextlib.contextmanager
def selenium_driver() -> t.Iterator[WebDriver]:
    """Context manager for a Selenium web scraper."""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def ensure_clickable(
    driver: WebDriver, by: str, identifier: str, timeout: float = 20.0
) -> WebElement:
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, identifier))
    )
    return element


def main():
    with selenium_driver() as driver:
        driver.get("https://selenium.dev/documentation")
        assert "Selenium" in driver.title

        elem = driver.find_element(By.ID, "m-documentationwebdriver")
        elem.click()
        assert "WebDriver" in driver.title


if __name__ == "__main__":
    main()
