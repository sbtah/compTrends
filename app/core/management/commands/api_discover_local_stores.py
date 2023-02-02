from crawler.logic.api_crawler import ApiCrawler
from crawler.options.endpoints import LOCAL_STORES_ENDPOINT
from django.core.management.base import BaseCommand
from stores.builders import api_update_or_create_local_store
from stores.models import EccommerceStore, LocalStore
from utilites.logger import logger
from datetime import date


def fetch_local_stores(parrent_domain):
    """
    Discover LocalStore by requesting LOCAL_STORES_ENDPOINT endpoint.
    """
    try:
        parrent_e_store = EccommerceStore.objects.get(domain=parrent_domain)
    except EccommerceStore.DoesNotExist:
        logger.error("No EccomerceStore found. Creating...")
        parrent_e_store = EccommerceStore.objects.create(
            domain=parrent_domain, main_url=f"http://{parrent_domain}/"
        )
    finally:
        crawler = ApiCrawler()
        stores = crawler.get_local_stores(local_stores_endpoint=LOCAL_STORES_ENDPOINT)
        if stores:
            for store in stores:
                store_name = store.get("name")
                store_id = store.get("selected_shop_store_view")
                last_scraped = date.today()
                api_update_or_create_local_store(
                    parrent_eccomerce_store=parrent_e_store,
                    name=store_name,
                    scraped_id=store_id,
                    last_scrape=last_scraped,
                )
        else:
            logger.error(f"Failed requesting URL: {LOCAL_STORES_ENDPOINT}")
            pass


class Command(BaseCommand):
    """Main class for command object that imports LocalStores from Api."""

    def add_arguments(self, parser):
        parser.add_argument(
            "parrent_store_domain",
            type=str,
            help="Searches parrent EccommerceStore by domain.",
        )

    def handle(self, *args, **options):
        """Custom handle method."""

        parrent_domain = options["parrent_store_domain"]
        number_of_local_stores_start = LocalStore.objects.all().count()
        self.stdout.write(
            self.style.WARNING(
                f"""
                Discovery of LocalStores started ...
                Current number of LocalStores: {number_of_local_stores_start}
                """
            )
        )
        fetch_local_stores(parrent_domain=parrent_domain)
        number_of_local_stores_finish = LocalStore.objects.all().count()
        new_stores = number_of_local_stores_finish - number_of_local_stores_start
        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Discovery of LocalStores finished.
                Current number of LocalStores: {number_of_local_stores_finish}
                Found: {new_stores} new LocalStores since last discovery process
                """
            )
        )
