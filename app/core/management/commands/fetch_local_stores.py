from django.core.management.base import BaseCommand
from crawler.logic.api_crawler import ApiCrawler
from stores.models import LocalStore, EccommerceStore
from stores.builders import api_update_or_create_local_store
from utilites.logger import logger


LOCAL_STORES_ENDPOINT = "https://www.castorama.pl/api/rest/headless/public/markets"


def fetch_local_stores(parrent_domain):
    try:
        parrent_e_store = EccommerceStore.objects.get(domain=parrent_domain)
        crawler = ApiCrawler()
        stores = crawler.get_local_stores(local_stores_endpoint=LOCAL_STORES_ENDPOINT)
        for store in stores:
            store_name = store.get("name")
            store_id = store.get("selected_shop_store_view")
            api_update_or_create_local_store(
                parrent_eccomerce_store=parrent_e_store,
                name=store_name,
                scraped_id=store_id,
            )
    except EccommerceStore.DoesNotExist:
        logger.error("No parrent EccommerceStore found. Quiting...")


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
                f"Fetching LocalStores started. Current LocalStores number: {LocalStore.objects.all().count()}"  # noqa
            )
        )
        fetch_local_stores(parrent_domain=parrent_domain)
        self.stdout.write(
            self.style.SUCCESS(
                f"Fetching LocalStores finished. Current LocalStores number: {LocalStore.objects.all().count()}"  # noqa
            )
        )
