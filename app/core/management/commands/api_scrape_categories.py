from categories.models import Category
from django.core.management.base import BaseCommand
from crawler.logic.data_scraper import DataApiScraper


class Command(BaseCommand):
    """Main class for command object that imports Categories from Api."""

    def handle(self, *args, **options):
        """Custom handle method."""

        number_of_categories_start = Category.objects.all().count()
        self.stdout.write(
            self.style.WARNING(
                f"""
                Discovery of Categories started ...
                Current number of Categories: {number_of_categories_start}
                """
            )
        )

        DataApiScraper().scrape_main_categories()
        DataApiScraper().scrape_child_categories()

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
