from django.core.management.base import BaseCommand
from handler.logic.website_operator import LocalStoreOperator
from products.models import Product, ProductLocalData
from stores.models import LocalStore
from stores.models import EccommerceStore
from crawler.options.endpoints import DOMAIN
import pandas as pd
import datetime
from crawler.helpers.time_it import calculate_time
from utilities.logger import logger


class Command(BaseCommand):
    """Main class for command object that imports Products from Api."""

    def handle(self, *args, **options):
        """Custom handle method."""

        # TODO:
        # Create product rapports for LocalStore.
        # active_stores = LocalStore.objects.filter(is_active=True)
        # for store in active_stores:
        #     operator = LocalStoreOperator(local_store_id=store.scraped_id)
        #     operator.create_monthly_active_products_rapport()

        # # TODO:
        # # Update products rapport with active Product data for each store.
        # active_stores = LocalStore.objects.filter(is_active=True)
        # for store in active_stores:
        #     operator = LocalStoreOperator(local_store_id=store.scraped_id)
        #     df = operator.open_xlsx_file(directory=operator.current_month_rapport_path)
        #     operator.add_missing_product_rows_to_rapport(data_frame=df)

        # TODO:
        # Update products rapport with LocalData for entire month.
        active_stores = LocalStore.objects.filter(is_active=True)
        for store in active_stores:
            operator = LocalStoreOperator(local_store_id=store.scraped_id)
            df = operator.open_xlsx_file(directory=operator.current_month_rapport_path)
            start_date = datetime.datetime.strptime(
                operator.current_month_year, operator.MONTH_DATE_FORMAT
            )
            end_date = datetime.datetime.strptime(
                operator.current_day_month_year, operator.DAY_DATE_FORMAT
            )
            delta = datetime.timedelta(days=1)
            while start_date <= end_date:
                # print(start_date)
                # print(start_date.strftime(operator.DAY_DATE_FORMAT))
                operator.add_stock_and_price_columns_to_rapport(
                    data_frame=df,
                    store_id=operator.local_store_id,
                    date=start_date.strftime(operator.DAY_DATE_FORMAT),
                )
                start_date += delta

        # TODO:
        # Implement creation of series for date.
        # start_date = datetime.datetime.strptime(
        #     operator.current_month_year, operator.MONTH_DATE_FORMAT
        # )
        # end_date = datetime.datetime.strptime(
        #     operator.current_day_month_year, operator.DAY_DATE_FORMAT
        # )
        # delta = datetime.timedelta(days=1)
        # while start_date <= end_date:
        #     # print(start_date)
        #     # print(start_date.strftime(operator.DAY_DATE_FORMAT))
        #     operator.add_stock_and_price_columns_to_rapport(
        #         data_frame=df,
        #         store_id=local_store.scraped_id,
        #         date_str=start_date.strftime(operator.DAY_DATE_FORMAT),
        #     )
        #     start_date += delta
