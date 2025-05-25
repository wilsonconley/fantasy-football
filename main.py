from __future__ import annotations

import contextlib
import enum
import typing as t
from dataclasses import dataclass
from decimal import Decimal

import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

import db

# ============
# Selenium
# ============


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


# ============
# Data Schema
# ============


class Position(enum.Enum):
    QB = enum.auto()
    RB = enum.auto()
    WR = enum.auto()
    TE = enum.auto()
    K = enum.auto()
    DST = enum.auto()


@dataclass(frozen=True)
class Player:
    name: str
    pos: Position
    rank: int
    pts: float

    def to_item_api(self) -> t.Mapping[str, t.Any]:
        return {
            "name": self.name,
            "pos": self.pos.name,
            "rank": self.rank,
            "pts": Decimal(str(self.pts)),
        }


def parse_player_row(player_row: WebElement, pos: Position) -> Player:
    return Player(
        name=player_row.find_element(By.CLASS_NAME, "player-cell-name").text,
        pos=pos,
        rank=int(player_row.find_element(By.CLASS_NAME, "sticky-cell-one").text),
        # "proj_pts": float(player_row.find_element(By.CLASS_NAME, "player-pts").text),
        pts=0.0,
    )


# ============
# Main
# ============


def main(webpages: dict[Position, list[str]]) -> list[Player]:
    rankings = []
    with selenium_driver() as driver:
        for position in webpages:
            for webpage in webpages[position]:
                # Go to the rankings page
                driver.get(webpage)

                # Find the ranking table
                ranking_table = driver.find_element(By.ID, "ranking-table")

                # Parse each player with their rank from the table
                rankings.extend(
                    [
                        parse_player_row(row, position)
                        for row in ranking_table.find_elements(
                            By.CLASS_NAME, "player-row"
                        )
                    ]
                )

    # Add rankings to db
    print(rankings)
    return rankings


if __name__ == "__main__":
    # Set season / week
    season = "2025"
    week = "week_1"

    # Aggregate ranking websites for each position group
    webpages = {  # TODO: adapter class
        Position.QB: ["https://www.fantasypros.com/nfl/rankings/qb.php"],
        # Position.RB: ["https://www.fantasypros.com/nfl/rankings/rb.php"],
        # Position.WR: ["https://www.fantasypros.com/nfl/rankings/wr.php"],
        # Position.TE: ["https://www.fantasypros.com/nfl/rankings/te.php"],
        # Position.K: ["https://www.fantasypros.com/nfl/rankings/k.php"],
        # Position.DST: ["https://www.fantasypros.com/nfl/rankings/dst.php"],
    }
    rankings = main(webpages)

    # Save weekly rankings to database
    with db.rankings_table(season, week) as table:
        for player in rankings:
            table.put_item(Item=player.to_item_api())
