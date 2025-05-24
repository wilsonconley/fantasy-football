from __future__ import annotations

import contextlib
import typing as t
from dataclasses import dataclass

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


@dataclass(frozen=True)
class Player:
    name: str
    rank: int
    pts: float


def parse_player_row(player_row: WebElement) -> Player:
    return Player(
        name=player_row.find_element(By.CLASS_NAME, "player-cell-name").text,
        rank=int(player_row.find_element(By.CLASS_NAME, "sticky-cell-one").text),
        # "proj_pts": float(player_row.find_element(By.CLASS_NAME, "player-pts").text),
        pts=0.0,
    )


def main():
    with selenium_driver() as driver:
        # Go to the rankings page
        driver.get("https://www.fantasypros.com/nfl/rankings/qb.php")
        assert "Fantasy Football Rankings" in driver.title

        # Find the ranking table
        ranking_table = driver.find_element(By.ID, "ranking-table")

        # Parse each player with their rank from the table
        rankings = [
            parse_player_row(row)
            for row in ranking_table.find_elements(By.CLASS_NAME, "player-row")
        ]

        print(rankings)


if __name__ == "__main__":
    main()
