from crawler.logic.data_scraper import DataApiScraper
from django.core.management.base import BaseCommand
from products.models import ProductLocalData


class Command(BaseCommand):
    """Main class for command object that imports Products from Api."""

    def handle(self, *args, **options):
        """Custom handle method."""

        self.stdout.write(
            self.style.WARNING(
                f"Scraping of ProductLocalData started. Current number of ProductLocalData: {ProductLocalData.objects.all().count()}"  # noqa
            )
        )
        DataApiScraper().scrape_product_local_data()
        self.stdout.write(
            self.style.SUCCESS(
                f"Scraping o ProductLocalData finished. Current number of ProductLocalData: {ProductLocalData.objects.all().count()}"  # noqa
            )
        )
