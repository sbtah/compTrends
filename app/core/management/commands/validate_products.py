from crawler.logic.data_scraper import DataApiScraper
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Main class for command object that imports Products from Api."""

    def handle(self, *args, **options):
        """Custom handle method."""

        self.stdout.write(
            self.style.WARNING(f"Validation process for Products started.")
        )
        DataApiScraper().validate_products_urls()
        self.stdout.write(
            self.style.SUCCESS(f"Validation process for Products finished.")
        )
