import typing as t
from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver

from schema import Player, Ranking, Website


class BaseScraper(ABC):
    """A base class for scraping player rankings from a website."""

    def __init__(self, name: Website):
        """Track the name of the website used to generate these rankings."""
        self.name = name

    @abstractmethod
    def load(self, driver: WebDriver) -> t.Mapping[Player, Ranking]:
        """Load player rankings from this website."""
        pass
