from random import choice
from typing import List, Tuple
import asyncio
import httpx
from crawler.helpers.randoms import random_sleep_small
from utilities.logger import logger
from crawler.options.settings import USER_AGENTS


class BaseApiCrawler:
    """
    Simple crawler used for requesting APIs.
    """

    def __init__(self, logger=logger):
        self.logger = logger

    @classmethod
    def get_random_user_agent(cls, user_agent_list: List[str]) -> str:
        """
        Return str with random User-Agent.
        - :arg user_agent_list: List of strings with User Agents.
        """
        agent = choice(user_agent_list)
        return agent

    @property
    def user_agent(self) -> str:
        agent = self.get_random_user_agent(USER_AGENTS)
        return agent

    def get(self, url: str) -> str:
        """
        Requests specified url synchronously. Returns JSON.
        - :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            res = httpx.get(url, timeout=30, headers=headers)
            random_sleep_small()
            return res.json()
        except httpx._exceptions.TimeoutException:
            self.logger.error("Connection was timed out.")
            return None
        except httpx._exceptions.ConnectError:
            self.logger.error("Connection Error.")
            return None
        except httpx._exceptions.HTTPError:
            self.logger.error("HTTPError was raised.")
            return None
        except Exception as e:
            self.logger.error(f"(get) Exception: {e}")
            return None

    async def async_get(self, client: httpx.AsyncClient, url: str) -> str:
        """
        Requests specified URL asynchronously. Returns JSON.
        - :arg client: Asynchronous client.
        - :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            res = await client.get(url, headers=headers)
            return res.json()
        except Exception as e:
            self.logger.error(f"(async_get) Exception: {e}")
            return None

    async def async_get_response_for_url(
        self, client: httpx.AsyncClient, url: str
    ) -> Tuple[str, str]:
        """
        Requests specified URL asynchronously.
        Returns Response and requested URL.
        - :arg client: Asynchronous client.
        - :arg url: Requested URL.
        """
        headers = {"User-Agent": f"{self.user_agent}"}
        try:
            res = await client.get(url, headers=headers)
            return (url, res)
        except Exception as e:
            self.logger.error(f"(async_get) Exception: {e}")
            return None
