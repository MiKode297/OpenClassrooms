"""Module."""

from abc import ABC, abstractmethod


class Website(ABC):
    """Web site."""

    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url

    # @property
    # @abstractmethod
    # def url(self):
    #     """property."""
    #     return "url"

    # @abstractmethod
    # def noofsides(self):
    #     """example."""
    #     pass


class OpenClassrooms(Website):
    """Self-explanatory"""

    URL_BASE = "https://openclassrooms.com"
    SEARCH_URI = "fr/search?page="

    def __init__(self, base_url: str = URL_BASE) -> None:

        super().__init__(base_url)
        self.azert = 12
