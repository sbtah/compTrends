from crawler.logic.data_scraper import DataApiScraper
from django.core.management.base import BaseCommand
from stores.models import LocalStore


class Command(BaseCommand):
    """Main class for command object that imports LocalStores from Api."""

    def handle(self, *args, **options):
        """Custom handle method."""

        number_of_local_stores_start = LocalStore.objects.all().count()
        self.stdout.write(
            self.style.WARNING(
                f"""
                Discovery of LocalStores started ...
                Current number of LocalStores:
                 - {number_of_local_stores_start}
                """
            )
        )

        DataApiScraper().scrape_local_stores()

        number_of_local_stores_finish = LocalStore.objects.all().count()
        new_stores = (
            number_of_local_stores_finish - number_of_local_stores_start
        )  # noqa
        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Discovery of LocalStores finished.
                Current number of LocalStores:
                 - {number_of_local_stores_finish}
                Found:
                - {new_stores} new LocalStores since last discovery process
                """
            )
        )
