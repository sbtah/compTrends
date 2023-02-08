from categories.models import Category
from django.core.management.base import BaseCommand
from products.models import Product, ProductLocalData
from stores.models import LocalStore


class Command(BaseCommand):
    """Main class for command object."""

    def handle(self, *args, **options):
        """Custom handle method."""

        number_of_local_stores_start = LocalStore.objects.all().count()
        number_of_categories_start = Category.objects.all().count()
        number_of_products_start = Product.objects.all().count()

        self.stdout.write(
            self.style.WARNING(
                f"""

                !!! WARNING THIS PROCCESS WILL TAKE OVER 6 Hours !!!

                Discovery and scrape of data started ...
                Current number of LocalStores: {number_of_local_stores_start}
                Current number of Categories: {number_of_categories_start}
                Current number of Products: {number_of_products_start}
                """
            )
        )

        number_of_categories_finish = Category.objects.all().count()
        number_of_products_finish = Product.objects.all().count()
        number_of_local_stores_finish = LocalStore.objects.all().count()

        self.stdout.write(
            self.style.SUCCESS(
                f"""
                Discovery and scrape of data finished.
                Current number of LocalStores: {number_of_local_stores_finish}
                Current number of Categories: {number_of_categories_finish}
                Current number of Products: {number_of_products_finish}
                """
            )
        )
