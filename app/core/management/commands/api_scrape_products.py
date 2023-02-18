from django.core.management.base import BaseCommand
from crawler.logic.data_scraper import DataApiScraper
from products.models import Product


class Command(BaseCommand):
    """Main class for command object that imports Products from Api."""

    def handle(self, *args, **options):
        """Custom handle method."""

        number_of_products_start = Product.objects.all().count()
        self.stdout.write(
            self.style.WARNING(
                f"""
                Discovery of Products started ...
                Current number of Products: {number_of_products_start}
                """
            )
        )

        DataApiScraper().discover_and_scrape_products_by_id()

        number_of_products_finish = Product.objects.all().count()
        new_products = number_of_products_finish - number_of_products_start
        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Discovery of Products finished. 
                Current number of Products: {number_of_products_finish}
                Found:
                 - {new_products} new Products since last discovery process.
                """
            )
        )
