from handler.logic.base_operator import BaseOperator
from stores.models import LocalStore
from products.models import Product, ProductLocalData
import pathlib
import pandas as pd
import datetime


class LocalStoreOperator(BaseOperator):
    """
    LocalStore operator.
    Generates and updates rapports for LocalStores.
    """

    def __init__(self, local_store_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_store_id = local_store_id
        self.logger.info(f"Started operator for : '{str(self.local_store_id)}'")

    @property
    def local_store_directory(self):
        if self.local_store_id is not None:
            return self.DATA_ROOT_DIR / str(self.local_store_id)
        else:
            return self.DATA_ROOT_DIR

    @property
    def current_month_rapport_pattern(self):
        return f"{str(self.local_store_id)}.{self.current_month_year}.xlsx"

    @property
    def current_price_column_name(self):
        return f"{self.current_day_month_year}:Cena"

    @property
    def current_stock_column_name(self):
        return f"{self.current_day_month_year}:Ilość"

    @property
    def current_month_rapport_path(self):
        return self.local_store_directory / self.current_month_rapport_pattern

    def format_string_to_date(self, date_str: str):
        """
        Converts string into date object with desired operator format.
        """
        date_object = datetime.datetime.strptime(date_str, self.DAY_DATE_FORMAT)
        return date_object

    def find_directory_for_store(self):
        """
        Searches for specified website directory in data folder.
        Return directory path if successful.
        """
        store_directory = self.local_store_directory
        return self.find_directory(directory=store_directory)

    def create_directory_for_store(self):
        """
        Creates directory for website in data directory,
        where all rapports will be stored.
        """
        store_directory = self.local_store_directory
        return self.create_directory(directory=store_directory)

    def search_store_directory_for_current_rapport(self):
        """"""
        path = self.search_directory_for_file(
            directory=self.local_store_directory,
            filename=self.current_month_rapport_pattern,
        )
        return path

    def create_xlsx_active_products_rapport(self):
        """
        Creates rapport of all Products data.
        Return pandas DataFrame.
        """
        if not self.find_directory(directory=self.current_month_rapport_path):
            product_query = Product.objects.filter(is_active=True)[25:]
            items = []
            for product in product_query:
                self.logger.info(f"Generating rapport for: {product}")
                data = {
                    "Nazwa": product.name,
                    "Castorama ID": product.scraped_id,
                    "Adres URL": product.url,
                    "SKU": product.sku,
                    "EAN": product.ean,
                    "Cena Podstawowa": product.default_price,
                    "Jednostka": product.unit_type,
                    "Konwersja": product.conversion,
                    "Konwersja Jednostkowa": product.conversion_unit,
                    "Ilość w opakowaniu": product.qty_per_package,
                    "Stawka VAT": product.tax_rate,
                }
                items.append(data)
            self.logger.info("Saving rapport ...")
            df = pd.DataFrame(items)
            try:
                df.to_excel(
                    self.current_month_rapport_path,
                    index=False,
                    sheet_name=f"{self.current_month_year}",
                )
                return df
            except OSError:
                self.create_directory_for_store()
                df.to_excel(
                    self.current_month_rapport_path,
                    index=False,
                    sheet_name=f"{self.current_month_year}",
                )
                return df
            except Exception as e:
                self.logger.error(
                    f"(create_xlsx_active_products_rapport) Some other Exception: {e}"
                )
        else:
            self.logger.error("Rapport for this store and month already exists.")

    def _find_missing_ids_in_xlsx_rapport(
        self,
        data_frame: pd.DataFrame,
    ) -> set:
        """
        Given the DataFrame, compares current XLSX rapport for active Products.
        Returns set of IDs that are active but not in rapport.
        - :arg data_frame: Pandas DataFrame (current rapport)
        """
        current_active_ids = set(
            [product.scraped_id for product in Product.objects.filter(is_active=True)]
        )
        file_ids = set(data_frame["Castorama ID"].to_list())
        missing_ids = current_active_ids.difference(file_ids)
        self.logger.info(f"Found: {len(missing_ids)} missing IDs. Returning ...")
        return missing_ids

    def add_missing_product_rows_to_rapport(
        self,
        data_frame: pd.DataFrame,
    ) -> None:
        """
        Searches provided DataFrame for missing rows of active Products.
        Adds any missing Product data.
        """
        missing_ids = self._find_missing_ids_in_xlsx_rapport(data_frame=data_frame)
        if missing_ids:
            items = []
            for id in missing_ids:
                product = Product.objects.get(scraped_id=id)
                data = {
                    "Nazwa": product.name,
                    "Castorama ID": product.scraped_id,
                    "Adres URL": product.url,
                    "SKU": product.sku,
                    "EAN": product.ean,
                    "Cena Podstawowa": product.default_price,
                    "Jednostka": product.unit_type,
                    "Konwersja": product.conversion,
                    "Konwersja Jednostkowa": product.conversion_unit,
                    "Ilość w opakowaniu": product.qty_per_package,
                    "Stawka VAT": product.tax_rate,
                }
                items.append(data)
            data_df = pd.DataFrame(items)
            new_df = pd.concat([data_frame, data_df])
            try:
                new_df.to_excel(
                    self.current_month_rapport_path,
                    index=False,
                    sheet_name=f"{self.current_month_year}",
                )
                self.logger.info("Saving Product data to rapport.")
            except Exception as e:
                self.logger.error(
                    f"(add_missing_product_data_to_rapport) Some other Exception: {e}"
                )
        else:
            self.logger.error("No extra active IDs in rapport were found...")

    def add_stock_and_price_columns_to_rapport(
        self,
        data_frame: pd.DataFrame,
        store_id: int,
        date: str | datetime.datetime.date,
    ):
        """
        Process DataFrame with Product data.
        Add columns: with current stock and price for LocalStore.
        - :arg data_frame: Pandas DataFrame object. XLSX rapport with Products.
        - :arg store_id: LocalStore ID (scraped_id).
        - :arg date: Date for which the collumns will be added.
        """
        if self.current_price_column_name in set(
            data_frame.columns
        ) or self.current_stock_column_name in set(data_frame.columns):
            self.logger.error(
                "Looks like this rapport already have stock and price data for provided date. Passing..."
            )
        else:
            if isinstance(date, str):
                date_time_obj = self.format_string_to_date(date_str=date)
            else:
                date_time_obj = date

            local_store = LocalStore.objects.get(scraped_id=store_id)

            def return_current_stock_for_store(value):
                """
                Helper function that is used by pandas apply.
                Adds stock for current value (Product)
                """
                parrent_product = Product.objects.get(scraped_id=value)
                try:
                    local = parrent_product.productlocaldata_set.get(
                        local_store_name=local_store.name,
                        last_scrape=date_time_obj,
                    )
                    self.logger.info(
                        f"Found current quantity for {parrent_product}. Returning: {local.quantity}"
                    )
                    return local.quantity
                except ProductLocalData.DoesNotExist:
                    self.logger.info(
                        f"No current quantity for {parrent_product}. Returning: No Data"
                    )
                    return "No Data"

            def return_current_price_for_store(value):
                """
                Helper function that is used by pandas apply.
                Adds price for current value (Product)
                """
                parrent_product = Product.objects.get(scraped_id=value)
                try:
                    local = parrent_product.productlocaldata_set.get(
                        local_store_name=local_store.name,
                        last_scrape=date_time_obj,
                    )
                    self.logger.info(
                        f"Found current price for {parrent_product}. Returning: {local.price}"
                    )
                    return local.price
                except ProductLocalData.DoesNotExist:
                    self.logger.info(
                        f"No current quantity for {parrent_product}. Returning: No Data"
                    )
                    return "No Data"

            data_frame[f"{date}:Ilość"] = data_frame["Castorama ID"].apply(
                return_current_stock_for_store
            )
            data_frame[f"{date}:Cena"] = data_frame["Castorama ID"].apply(
                return_current_price_for_store
            )
            data_frame.to_excel(
                self.current_month_rapport_path,
                index=False,
                sheet_name=f"{self.current_month_year}",
            )
