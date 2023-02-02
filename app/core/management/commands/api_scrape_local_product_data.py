from products.models import Product, ProductLocalData
from stores.models import EccommerceStore, LocalStore
from crawler.logic.api_crawler import ApiCrawler
from django.core.management.base import BaseCommand
from utilites.logger import logger
from datetime import date
from crawler.helpers.mapper import generate_ids_map
from crawler.options.endpoints import (
    SINGLE_PRODUCT_BY_ID,
    SINGLE_PRODUCT_BY_ID_FOR_STORE_ID,
)
import asyncio


def generate_local_stores_ids(parrent_domain):
    """"""
    local_stores_ids = LocalStore.objects.filter(
        parrent_store__domain=parrent_domain,
    )
    return [store.scraped_id for store in local_stores_ids]


def generate_products_ids(parrent_domain):
    """"""
    product_ids = Product.objects.filter(
        parrent_store__domain=parrent_domain,
    )
    return [product.scraped_id for product in product_ids]


def scrape_product_local_data(parrent_domain):
    """"""

    parrent_e_store = EccommerceStore.objects.get(domain=parrent_domain)
    crawler = ApiCrawler()
    products_ids_genex = generate_products_ids(parrent_domain=parrent_domain)
    local_stores_ids_genex = generate_local_stores_ids(parrent_domain=parrent_domain)

    for id in products_ids_genex:
        parrent_product = Product.objects.get(scraped_id=id)
        products_local_data_feature = asyncio.run(
            crawler.get_products_by_ids_for_local_store(
                product_id=id,
                single_product_by_id_for_store_id_url=SINGLE_PRODUCT_BY_ID_FOR_STORE_ID,
                range_of_product_ids=local_stores_ids_genex,
            )
        )
        for product_local_data in products_local_data_feature:
            if product_local_data and isinstance(product_local_data, dict):
                print(product_local_data)


class Command(BaseCommand):
    """Main class for command object that imports Products from Api."""

    def add_arguments(self, parser):
        parser.add_argument(
            "parrent_store_domain",
            type=str,
            help="Searches parrent EccommerceStore by domain. All created Localstores will be added as childs.",  # noqa
        )

    def handle(self, *args, **options):
        """Custom handle method."""

        parrent_domain = options["parrent_store_domain"]

        self.stdout.write(
            self.style.WARNING(
                f"Fetching ProductLocalData started. Current number of ProductLocalData: {ProductLocalData.objects.all().count()}"  # noqa
            )
        )
        scrape_product_local_data(parrent_domain=parrent_domain)
        self.stdout.write(
            self.style.SUCCESS(
                f"Fetching ProductLocalData finished. Current number of ProductLocalData: {ProductLocalData.objects.all().count()}"  # noqa
            )
        )
