from crawler.logic.api_crawler import ApiCrawler
from crawler.options.endpoints import LOCAL_STORES_ENDPOINT
from django.core.management.base import BaseCommand
from stores.builders import api_update_or_create_local_store
from stores.models import EccommerceStore, LocalStore
from utilites.logger import logger
from django.utils import timezone


def fetch_local_stores(parrent_domain):
    """
    Discover LocalStore by requesting proper endpoint.
    """
    try:
        parrent_e_store = EccommerceStore.objects.get(domain=parrent_domain)
    except EccommerceStore.DoesNotExist:
        logger.error("No EccomerceStore found. Creating...")
        parrent_e_store = EccommerceStore.objects.create(
            domain=parrent_domain, main_url=f"http://{parrent_domain}/"
        )
        crawler = ApiCrawler()
        stores = crawler.get_local_stores(local_stores_endpoint=LOCAL_STORES_ENDPOINT)
        if stores:
            for store in stores:
                store_name = store.get("name")
                store_id = store.get("selected_shop_store_view")
                last_scraped = timezone.now()
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
    """Main class for command object that imports products from shoper."""

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
                f"Fetching LocalStores started. Current number of LocalStores: {LocalStore.objects.all().count()}"  # noqa
            )
        )
        fetch_local_stores(parrent_domain=parrent_domain)
        self.stdout.write(
            self.style.SUCCESS(
                f"Fetching LocalStores finished. Current number of LocalStores: {LocalStore.objects.all().count()}"  # noqa
            )
        )
