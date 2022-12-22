"""Module."""

from enum import Enum, auto

from abc import ABC, abstractmethod

from typing import Optional


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
        self.post_lst = []


class WebsitePost(Website):
    """Web site post."""

    class PostType(Enum):
        """Self-explanatory"""

        COURSE = auto()
        PATH = auto()

    def __init__(self, uri: str = "", parent: Optional[OpenClassrooms] = None) -> None:

        super().__init__()

        self.parent = parent
        self.uri = uri
        self.identifier = ""
        self.type = None
        self.theme = ""
        self.title = ""
        self.level = ""
        self.period = ""
        self.period_unit = ""
        self.description = ""
        self.category = ""


class Path(WebsitePost):
    """Web site post."""

    def __init__(self, base_url: str = "") -> None:
        super().__init__(base_url)
        self.website = base_url


class Course(WebsitePost):
    """Web site post."""

    def __init__(self, base_url: str = "") -> None:
        super().__init__(base_url)
        self.website = base_url
