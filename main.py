from __future__ import annotations

import contextlib
import typing as t
from dataclasses import asdict
from decimal import Decimal

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

import db
from base import BaseScraper
from fantasypros import FantasyPros
from schema import Player, Ranking, DBItem, DBRanking


@contextlib.contextmanager
def selenium_driver() -> t.Iterator[WebDriver]:
    """Context manager for a Selenium web scraper."""
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def scrape(websites: t.Sequence[BaseScraper]) -> t.Mapping[Player, t.Sequence[Ranking]]:
    """Scrape all websites to aggregate rankings."""
    rankings: dict[Player, list[Ranking]] = {}
    with selenium_driver() as driver:
        for website in websites:
            for player, ranking in website.load(driver).items():
                if player not in rankings:
                    rankings[player] = [ranking]
                else:
                    rankings[player].append(ranking)
    return rankings


def main():
    # Set season / week
    season = "2025"
    week = "week_1"

    # Scrape all ranking websites
    websites = [
        FantasyPros(),
    ]
    all_rankings = scrape(websites)

    # Save weekly rankings to database
    with db.rankings_table(season, week) as table:
        for player, rankings in all_rankings.items():
            table.put_item(
                Item=asdict(
                    DBItem(
                        name=player.name,
                        pos=player.pos.name,
                        rankings={
                            ranking.website: DBRanking(
                                rank=ranking.rank,
                                proj_pts=Decimal(str(ranking.proj_pts)),
                            )
                            for ranking in rankings
                        },
                    )
                )
            )


if __name__ == "__main__":
    main()
