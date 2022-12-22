"""Module."""


from abc import ABC, abstractmethod


class Website(ABC):
    """Web site."""

    def __init__(self, base_url: str = "") -> None:
        self.base_url = base_url
        self.driver = None
        self.content = None

    @abstractmethod
    def get_posts(self):
        """Get all website articles/posts"""

    # @abstractmethod
    # def init_driver(self, driver_type, timeout: int):

    #     if driver_type == 0:
    #         driver = WebsiteDriver(timeout)
    #         # self.driver.timeout_s = 12

    #     self.driver = driver

    # @property
    # @abstractmethod
    # def url(self):
    #     """property."""
    #     return "url"
