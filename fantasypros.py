import typing as t

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from base import BaseScraper
from schema import Player, Position, Ranking


class FantasyPros(BaseScraper):
    """A class for scraping player rankings from FantasyPros."""

    def __init__(self):
        """Track the name of the website used to generate these rankings."""
        super().__init__(name="fantasypros")

    def load(self, driver: WebDriver) -> t.Mapping[Player, Ranking]:
        """Load player rankings from this website."""
        players = {}

        # Go to the rankings page for each position
        webpages = {
            Position.QB: "https://www.fantasypros.com/nfl/rankings/qb.php",
            # Position.RB: "https://www.fantasypros.com/nfl/rankings/rb.php",
            # Position.WR: "https://www.fantasypros.com/nfl/rankings/wr.php",
            # Position.TE: "https://www.fantasypros.com/nfl/rankings/te.php",
            # Position.K: "https://www.fantasypros.com/nfl/rankings/k.php",
            # Position.DST: "https://www.fantasypros.com/nfl/rankings/dst.php",
        }
        for position, webpage in webpages.items():
            # Navigate to page
            driver.get(webpage)

            # Find the ranking table
            ranking_table = driver.find_element(By.ID, "ranking-table")

            # Parse each player with their rank from the table
            for row in ranking_table.find_elements(By.CLASS_NAME, "player-row"):
                # Grab each relevant field
                name = row.find_element(By.CLASS_NAME, "player-cell-name").text
                rank = int(row.find_element(By.CLASS_NAME, "sticky-cell-one").text)
                proj_pts = 0.0  # float(player_row.find_element(By.CLASS_NAME, "player-pts").text)

                # Players only have one position, so we don't need to check if the
                # player has already been added to the dict here
                players[Player(name, position)] = Ranking(self.name, rank, proj_pts)

        return players
