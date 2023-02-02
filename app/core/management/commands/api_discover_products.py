import asyncio

from crawler.helpers.mapper import generate_ids_map
from crawler.logic.api_crawler import ApiCrawler
from crawler.options.endpoints import SINGLE_PRODUCT_BY_ID
from django.core.management.base import BaseCommand
from datetime import date
from products.builders import api_update_or_create_product
from products.models import Product
from stores.models import EccommerceStore
from utilites.logger import logger


def discover_products_by_id(parrent_domain):
    """
    Discover new Products while requesting SINGLE_PRODUCT_BY_ID endpoint.
    """
    parrent_e_store = EccommerceStore.objects.get(domain=parrent_domain)
    crawler = ApiCrawler()
    genex_of_genex = generate_ids_map()

    for generator in genex_of_genex:
        products_generator = asyncio.run(
            crawler.get_products_by_ids(
                range_of_product_ids=generator,
                single_product_by_id_url=SINGLE_PRODUCT_BY_ID,
            )
        )
        for product_data in products_generator:
            if product_data and isinstance(product_data, dict):
                if not "ins" or not "enc" in product_data.get("data").get("sku"):
                    name = product_data.get("data").get("name")
                    url = product_data.get("data").get("url_path")
                    scraped_id = product_data.get("data").get("entity_id")
                    api_url = SINGLE_PRODUCT_BY_ID.format(scraped_id)
                    short_description = (
                        ""
                        if product_data.get("data").get("short_description") is None
                        else product_data.get("data").get("short_description")
                    )
                    sku = product_data.get("data").get("sku")
                    ean = (
                        ""
                        if product_data.get("data").get("ean") is None
                        else product_data.get("data").get("ean")
                    )
                    brand_name = (
                        ""
                        if product_data.get("data").get("brand_data").get("name")
                        is None
                        else product_data.get("data").get("brand_data").get("name")
                    )
                    promotion = (
                        False
                        if product_data.get("data").get("info_boxes").get("promo_price")
                        is None
                        else True
                    )
                    default_price = product_data.get("data").get("default_price")
                    promo_price = product_data.get("data").get("promo_price")
                    unit_type = product_data.get("data").get("price_unit")
                    conversion = (
                        ""
                        if product_data.get("data").get("conversion") is None
                        else product_data.get("data").get("conversion")
                    )
                    conversion_unit = (
                        ""
                        if product_data.get("data").get("conversion_unit") is None
                        else product_data.get("data").get("conversion_unit")
                    )
                    qty_per_package = product_data.get("data").get("qty_per_package")
                    tax_rate = product_data.get("data").get("tax_rate")
                    try:
                        parrent_category_from_path = (
                            product_data.get("data").get("category_path")[-1].get("id")
                        )
                    except IndexError:
                        parrent_category_from_path = None
                    last_scrape = date.today()

                    api_update_or_create_product(
                        name=name,
                        url=url,
                        scraped_id=scraped_id,
                        api_url=api_url,
                        short_description=short_description,
                        sku=sku,
                        ean=ean,
                        brand_name=brand_name,
                        promotion=promotion,
                        default_price=default_price,
                        promo_price=promo_price,
                        unit_type=unit_type,
                        conversion=conversion,
                        conversion_unit=conversion_unit,
                        qty_per_package=qty_per_package,
                        tax_rate=tax_rate,
                        parrent_category_from_path=parrent_category_from_path,
                        parrent_eccomerce_store=parrent_e_store,
                        last_scrape=last_scrape,
                    )
            else:
                logger.error(f"Wrong response type: {product_data}")


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
        number_of_products_start = Product.objects.all().count()
        self.stdout.write(
            self.style.WARNING(
                f"""
                Discovery of Products started ...
                Current number of Products: {number_of_products_start}
                """
            )
        )
        discover_products_by_id(parrent_domain=parrent_domain)
        number_of_products_finish = Product.objects.all().count()
        new_products = number_of_products_finish - number_of_products_start
        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Discovery of Products finished. 
                Current number of Products: {number_of_products_finish}
                Found: {new_products} new Products since last discovery process.
                """
            )
        )
