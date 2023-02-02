from categories.builders import api_update_or_create_category
from categories.models import Category
from crawler.logic.api_crawler import ApiCrawler
from crawler.options.endpoints import (
    SINGLE_CATEGORY_BY_ID,
    CHILD_CATEGORIES_OF_BUDOWA,
    CHILD_CATEGORIES_OF_INSTALACJE,
    CHILD_CATEGORIES_OF_NARZEDZIA,
    CHILD_CATEGORIES_OF_OGROD,
    CHILD_CATEGORIES_OF_URZADZANIE,
    CHILD_CATEGORIES_OF_WYKONCZENIE,
    DEFAULT_CATEGORY,
    MAIN_CATEGORY_BUDOWA,
    MAIN_CATEGORY_INSTALACJE,
    MAIN_CATEGORY_NARZEDZIA,
    MAIN_CATEGORY_OGROD,
    MAIN_CATEGORY_URZADZANIE,
    MAIN_CATEGORY_WYKONCZENIE,
)
from django.core.management.base import BaseCommand
from stores.models import EccommerceStore
from utilites.logger import logger
from datetime import date


main_categories_urls_to_discover = [
    DEFAULT_CATEGORY,
    MAIN_CATEGORY_BUDOWA,
    MAIN_CATEGORY_INSTALACJE,
    MAIN_CATEGORY_NARZEDZIA,
    MAIN_CATEGORY_OGROD,
    MAIN_CATEGORY_URZADZANIE,
    MAIN_CATEGORY_WYKONCZENIE,
]
child_categories_urls_to_discover = [
    CHILD_CATEGORIES_OF_BUDOWA,
    CHILD_CATEGORIES_OF_INSTALACJE,
    CHILD_CATEGORIES_OF_NARZEDZIA,
    CHILD_CATEGORIES_OF_OGROD,
    CHILD_CATEGORIES_OF_URZADZANIE,
    CHILD_CATEGORIES_OF_WYKONCZENIE,
]


def discover_main_categories(parrent_domain):
    """
    Discover Categories in main_categories_urls_to_discover.
    """
    try:
        parrent_e_store = EccommerceStore.objects.get(domain=parrent_domain)
        crawler = ApiCrawler()
        for category_url in main_categories_urls_to_discover:
            category_data = crawler.get(url=category_url)
            if category_data:
                name = category_data[0].get("name")
                url = category_data[0].get("url")
                api_url = category_url
                scraped_id = category_data[0].get("id")
                meta_title = (
                    ""
                    if category_data[0].get("meta_title") is None
                    else category_data[0].get("meta_title")
                )
                category_path = category_data[0].get("path")
                category_level = category_data[0].get("level")
                children_category_count = category_data[0].get("children_count")
                product_count = category_data[0].get("product_count")
                parrent_store = parrent_e_store
                last_scrape = date.today()
                api_update_or_create_category(
                    parrent_eccomerce_store=parrent_store,
                    name=name,
                    url=url,
                    api_url=api_url,
                    scraped_id=scraped_id,
                    meta_title=meta_title,
                    category_path=category_path,
                    category_level=category_level,
                    children_category_count=children_category_count,
                    product_count=product_count,
                    last_scrape=last_scrape,
                )
            else:
                logger.error(f"Failed requesting URL: {category_url}")
                pass
    except EccommerceStore.DoesNotExist:
        logger.error("No parrent EccommerceStore found. Quiting...")


def discover_child_categories(parrent_domain):
    """
    Discover Categories in child_categories_urls_to_discover.
    """
    try:
        parrent_e_store = EccommerceStore.objects.get(domain=parrent_domain)
        crawler = ApiCrawler()
        for category_url in child_categories_urls_to_discover:
            child_categories_data = crawler.get(url=category_url)
            if child_categories_data:
                for category in child_categories_data:
                    name = category.get("name")
                    url = category.get("url")
                    api_url = SINGLE_CATEGORY_BY_ID.format(category.get("id"))
                    scraped_id = category.get("id")
                    meta_title = (
                        ""
                        if category.get("meta_title") is None
                        else category.get("meta_title")
                    )
                    category_path = category.get("path")
                    category_level = category.get("level")
                    children_category_count = category.get("children_count")
                    product_count = category.get("product_count")
                    parrent_store = parrent_e_store
                    last_scrape = date.today()
                    api_update_or_create_category(
                        parrent_eccomerce_store=parrent_store,
                        name=name,
                        url=url,
                        api_url=api_url,
                        scraped_id=scraped_id,
                        meta_title=meta_title,
                        category_path=category_path,
                        category_level=category_level,
                        children_category_count=children_category_count,
                        product_count=product_count,
                        last_scrape=last_scrape,
                    )
            else:
                logger.error(f"Failed requesting URL: {category_url}")
                pass
    except EccommerceStore.DoesNotExist:
        logger.error("No parrent EccommerceStore found. Quiting...")


class Command(BaseCommand):
    """Main class for command object that imports Categories from Api."""

    def add_arguments(self, parser):
        parser.add_argument(
            "parrent_store_domain",
            type=str,
            help="Searches parrent EccommerceStore by domain.",
        )

    def handle(self, *args, **options):
        """Custom handle method."""

        parrent_domain = options["parrent_store_domain"]
        number_of_categories_start = Category.objects.all().count()
        self.stdout.write(
            self.style.WARNING(
                f"""
                Discovery of Categories started ...
                Current number of Categories: {number_of_categories_start}
                """
            )
        )
        discover_main_categories(parrent_domain=parrent_domain)
        discover_child_categories(parrent_domain=parrent_domain)
        number_of_categories_finish = Category.objects.all().count()
        new_categories = number_of_categories_finish - number_of_categories_start
        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Discovery of Categories finished.
                Current number of Categories: {number_of_categories_finish}
                Found: {new_categories} new Categories since last discovery process. 
                """
            )
        )
