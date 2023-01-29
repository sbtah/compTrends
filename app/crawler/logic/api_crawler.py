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

    async def get_products_by_ids_for_local_store(
        self,
        local_store_id: int,
        single_product_by_id_for_store_id_url: str,
        range_of_product_ids: Iterator[int],
    ) -> Future[Dict]:
        """
        Sends requests to SINGLE_PRODUCT_BY_ID_FOR_STORE_ID asynchronously.
        - :arg local_store_id: Integer (ID) of local store.
        - :arg single_product_by_id_for_store_id_url: Api URL
            for for Product Data for Local Store.
        - :arg range_of_product_ids: Iterator of integers (IDs)
            that will be used while sending requests.
        """
        async with httpx.AsyncClient() as client:
            tasks = []
            for num in range_of_product_ids:
                print(f"RECEIVED ID: {num}")
                tasks.append(
                    asyncio.ensure_future(
                        self.async_get(
                            client,
                            single_product_by_id_for_store_id_url.format(
                                local_store_id, num
                            ),
                        )
                    )
                )
            products = await asyncio.gather(*tasks)
            return products
