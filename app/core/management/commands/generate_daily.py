from django.core.management.base import BaseCommand
from handler.logic.store_operator import LocalStoreOperator
from stores.models import LocalStore


def generate_daily():
    """
    Generate and update a daily rapports for all active LocalStores.
    """
    local_stores = LocalStore.objects.filter(is_active=True)
    for store in local_stores:
        operator = LocalStoreOperator(local_store_id=store.scraped_id)
        operator.create_monthly_active_products_rapport()
        operator.update_products_rapport_with_active_products()
        operator.update_products_rapport_with_current_daily_stock_and_price()


class Command(BaseCommand):
    """Main class for command object that imports Products from Api."""

    def handle(self, *args, **options):
        """Custom handle method."""

        self.stdout.write(
            self.style.WARNING(
                """
                Generating daily rapports for active stores started...
                """
            )
        )
        generate_daily()
        self.stdout.write(
            self.style.SUCCESS(
                """
                Daily rapports completed.
                """
            )
        )
