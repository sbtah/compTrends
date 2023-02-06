import asyncio
from asyncio import Future
from typing import Dict, Iterator, List

import httpx
from utilites.logger import logger
from crawler.logic.base_crawler import BaseApiCrawler


class ApiCrawler(BaseApiCrawler):
    """
    Specialized crawler that works with defined endpoints.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_local_stores(self, local_stores_endpoint: str) -> List[Dict]:
        """
        Requests local_stores_endpoint synchronously.
        Returns List of dictionaries with data of local stores.
        - :arg local_stores_endpoint: API Url with LocalStores data.
        """
        try:
            local_stores = self.get(url=local_stores_endpoint)
            return local_stores
        except Exception as e:
            logger.error(f"(get_local_stores) Exception: {e}")
            return None

    def get_single_product_by_id(self, product_id):
        """
        Requests SINGLE_PRODUCT_BY_ID endpoint synchronously.
        Returns JSON with Product data.
        - :arg product_id: Integer that will represent ID of Product.
        """
        pass

    async def get_products_by_urls(
        self,
        iterator_of_urls: Iterator[str],
    ) -> httpx.Response:
        """
        Sends requests to Product url asynchronously.
        - :arg iterator_of_urls: Iterator of Product URLS
            that will be used while sending requests.
        """
        async with httpx.AsyncClient() as client:
            tasks = []
            for url in iterator_of_urls:
                tasks.append(
                    asyncio.ensure_future(
                        self.async_get_response(
                            client,
                            url,
                        )
                    )
                )
            products = await asyncio.gather(*tasks)
            return products

    async def get_products_by_ids(
        self,
        range_of_product_ids: Iterator[int],
        single_product_by_id_url: str,
    ) -> Future[Dict]:
        """
        Sends requests to SINGLE_PRODUCT_BY_ID asynchronously.
        - :arg range_of_product_ids: Iterator of integers (IDs)
            that will be used while sending requests.
        - :arg single_product_by_id_url: API Url for Product Endopoint.
        """
        async with httpx.AsyncClient() as client:
            tasks = []
            for num in range_of_product_ids:
                tasks.append(
                    asyncio.ensure_future(
                        self.async_get(
                            client,
                            single_product_by_id_url.format(num),
                        )
                    )
                )
            products = await asyncio.gather(*tasks)
            return products

    async def get_products_by_ids_for_all_local_stores(
        self,
        product_id: int,
        single_product_by_id_for_store_id_url: str,
        iterator_of_stores_ids: Iterator[int],
    ) -> Future[Dict]:
        """
        Sends requests to SINGLE_PRODUCT_BY_ID_FOR_STORE_ID asynchronously.
        - :arg product_id: Integer (ID) of Product.
        - :arg single_product_by_id_for_store_id_url: Api URL
            for for Product Data for Local Store.
        - :arg iterator_of_stores_ids: Iterator of integers (LocalStores IDs)
            that will be used while sending requests.
        """
        async with httpx.AsyncClient() as client:
            tasks = []
            for store_id in iterator_of_stores_ids:
                tasks.append(
                    asyncio.ensure_future(
                        self.async_get(
                            client,
                            single_product_by_id_for_store_id_url.format(
                                store_id, product_id
                            ),
                        )
                    )
                )
            data = await asyncio.gather(*tasks)
            return data

    async def get_products_by_ids_for_local_store(
        self,
        store_id: int,
        single_product_by_id_for_store_id_url: str,
        iterator_of_product_ids: Iterator[int],
    ) -> Future[Dict]:
        """
        Sends requests to SINGLE_PRODUCT_BY_ID_FOR_STORE_ID asynchronously.
        - :arg store_id: Integer (ID) of LocalStore.
        - :arg single_product_by_id_for_store_id_url: Api URL
            for for Product Data for Local Store.
        - :arg iterator_of_product_ids: Iterator of integers (Products IDs)
            that will be used while sending requests.
        """
        async with httpx.AsyncClient() as client:
            tasks = []
            for product_id in iterator_of_product_ids:
                tasks.append(
                    asyncio.ensure_future(
                        self.async_get(
                            client,
                            single_product_by_id_for_store_id_url.format(
                                store_id, product_id
                            ),
                        )
                    )
                )
            data = await asyncio.gather(*tasks)
            return data
