import asyncio

from categories.builders import api_update_or_create_category
from crawler.helpers.extractors import (
    category_data_extract,
    local_store_data_extract,
    product_data_extract,
    product_local_data_extract,
)
from crawler.helpers.mapper import generate_ids_map
from crawler.logic.api_crawler import ApiCrawler
from crawler.options.endpoints import (
    CHILD_CATEGORIES_OF_BUDOWA,
    CHILD_CATEGORIES_OF_INSTALACJE,
    CHILD_CATEGORIES_OF_NARZEDZIA,
    CHILD_CATEGORIES_OF_OGROD,
    CHILD_CATEGORIES_OF_URZADZANIE,
    CHILD_CATEGORIES_OF_WYKONCZENIE,
    DEFAULT_CATEGORY,
    DOMAIN,
    LOCAL_STORES_ENDPOINT,
    MAIN_CATEGORY_BUDOWA,
    MAIN_CATEGORY_INSTALACJE,
    MAIN_CATEGORY_NARZEDZIA,
    MAIN_CATEGORY_OGROD,
    MAIN_CATEGORY_URZADZANIE,
    MAIN_CATEGORY_WYKONCZENIE,
    SINGLE_PRODUCT_BY_ID,
    SINGLE_PRODUCT_BY_ID_FOR_STORE_ID,
)
from products.builders import (
    api_update_or_create_product,
    api_update_or_create_product_local_data,
    validate_product_active,
)
from products.models import Product
from stores.builders import api_update_or_create_local_store
from stores.models import EccommerceStore, LocalStore
from utilities.time_it import calculate_time


class DataApiScraper(ApiCrawler):
    """
    Scrapes data from specified API Endpoints.
    """

    DOMAIN = DOMAIN
    LOCAL_STORES_ENDPOINT = LOCAL_STORES_ENDPOINT
    SINGLE_PRODUCT_BY_ID = SINGLE_PRODUCT_BY_ID
    SINGLE_PRODUCT_BY_ID_FOR_STORE_ID = SINGLE_PRODUCT_BY_ID_FOR_STORE_ID

    MAIN_CATEGORIES_URL = [
        DEFAULT_CATEGORY,
        MAIN_CATEGORY_BUDOWA,
        MAIN_CATEGORY_INSTALACJE,
        MAIN_CATEGORY_NARZEDZIA,
        MAIN_CATEGORY_OGROD,
        MAIN_CATEGORY_URZADZANIE,
        MAIN_CATEGORY_WYKONCZENIE,
    ]
    CHILD_CATEGORIES_URLS = [
        CHILD_CATEGORIES_OF_BUDOWA,
        CHILD_CATEGORIES_OF_INSTALACJE,
        CHILD_CATEGORIES_OF_NARZEDZIA,
        CHILD_CATEGORIES_OF_OGROD,
        CHILD_CATEGORIES_OF_URZADZANIE,
        CHILD_CATEGORIES_OF_WYKONCZENIE,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_active_local_stores_ids(self):
        """
        Helper method that returns list of Active LocalStores IDs.
        """
        local_stores_ids = LocalStore.objects.filter(
            parrent_store__domain=self.DOMAIN,
            is_active=True,
        )
        return [store.scraped_id for store in local_stores_ids]

    def generate_list_of_products_ids_list(self):
        """
        Generate List of Active Products IDs list.
        """
        stp = 100
        products = Product.objects.filter(
            parrent_store__domain=self.DOMAIN,
            is_active=True,
        )
        products_ids = [product.scraped_id for product in products]
        return [
            products_ids[x : x + stp] for x in range(0, len(products_ids), stp)  # noqa
        ]  # noqa

    def generate_list_of_products_urls_list(self):
        """
        Generate List of Products url list. Used for validation by url.
        """
        stp = 100
        products = Product.objects.filter(
            parrent_store__domain=self.DOMAIN,
        )
        products_ids = [product.url for product in products]
        return [
            products_ids[x : x + stp] for x in range(0, len(products_ids), stp)  # noqa
        ]  # noqa

    @calculate_time
    def scrape_local_stores(self):
        """
        Scrape LocalStores data by requesting Local Stores endpoint.
        """
        try:
            parrent_e_store = EccommerceStore.objects.get(domain=self.DOMAIN)
        except EccommerceStore.DoesNotExist:
            self.logger.error("No EccomerceStore found. Creating...")
            parrent_e_store = EccommerceStore.objects.create(
                domain=self.DOMAIN, main_url=f"http://{self.DOMAIN}/"
            )
        finally:
            stores = self.get_local_stores(
                local_stores_endpoint=self.LOCAL_STORES_ENDPOINT
            )
            if stores:
                if isinstance(stores, list):
                    for store in stores:
                        data = local_store_data_extract(store_response=store)
                        api_update_or_create_local_store(
                            parrent_eccomerce_store=parrent_e_store,
                            name=data.get("store_name"),
                            scraped_id=data.get("store_id"),
                            last_scrape=data.get("last_scrape"),
                        )
                else:
                    self.logger.error(
                        "Received wrong response from: get_local_stores."
                    )  # noqa
                    pass
            else:
                self.logger.error(
                    f"Failed requesting URL: {self.LOCAL_STORES_ENDPOINT}"
                )
                pass

    @calculate_time
    def scrape_main_categories(self):
        """
        Scrape Categories by requesting MAIN_CATEGORIES_URL endpoints.
        """
        try:
            parrent_e_store = EccommerceStore.objects.get(domain=self.DOMAIN)
            for main_category_url in self.MAIN_CATEGORIES_URL:
                category_data = self.get(url=main_category_url)
                if category_data:
                    if isinstance(category_data, list):
                        data = category_data_extract(
                            category_response=category_data[0]
                        )  # noqa
                        api_update_or_create_category(
                            parrent_eccomerce_store=parrent_e_store,
                            name=data.get("name"),
                            url=data.get("url"),
                            api_url=data.get("api_url"),
                            scraped_id=data.get("scraped_id"),
                            meta_title=data.get("meta_title"),
                            category_path=data.get("category_path"),
                            category_level=data.get("category_level"),
                            children_category_count=data.get(
                                "children_category_count"
                            ),  # noqa
                            product_count=data.get("product_count"),
                            last_scrape=data.get("last_scrape"),
                        )
                    else:
                        self.logger.error(
                            f"Received wrong response type: {category_data}"
                        )
                        pass
                else:
                    self.logger.error(
                        f"Failed requesting URL: {main_category_url}"
                    )  # noqa
                    pass
        except EccommerceStore.DoesNotExist:
            self.logger.error("No parrent EccommerceStore found. Quiting...")
            pass

    def scrape_child_categories(self):
        """
        Scrape Categories by requesting CHILD_CATEGORIES_URLS endpoints.
        """
        try:
            parrent_e_store = EccommerceStore.objects.get(domain=self.DOMAIN)
            for child_category_url in self.CHILD_CATEGORIES_URLS:
                child_categories_response = self.get(url=child_category_url)
                if child_categories_response:
                    if isinstance(child_categories_response, list):
                        for category_data in child_categories_response:
                            data = category_data_extract(
                                category_response=category_data
                            )
                            api_update_or_create_category(
                                parrent_eccomerce_store=parrent_e_store,
                                name=data.get("name"),
                                url=data.get("url"),
                                api_url=data.get("api_url"),
                                scraped_id=data.get("scraped_id"),
                                meta_title=data.get("meta_title"),
                                category_path=data.get("category_path"),
                                category_level=data.get("category_level"),
                                children_category_count=data.get(
                                    "children_category_count"
                                ),
                                product_count=data.get("product_count"),
                                last_scrape=data.get("last_scrape"),
                            )
                    else:
                        self.logger.error(
                            f"Received wrong response type: {child_categories_response}"  # noqa
                        )
                        pass
                else:
                    self.logger.error(
                        f"Failed requesting URL: {child_category_url}"
                    )  # noqa
                    pass
        except EccommerceStore.DoesNotExist:
            self.logger.error("No parrent EccommerceStore found. Quiting...")
            pass

    @calculate_time
    def discover_and_scrape_products_by_id(self):
        """
        Discover Product while requesting SINGLE_PRODUCT_BY_ID.
        Scrape Product data.
        """
        try:
            parrent_e_store = EccommerceStore.objects.get(domain=self.DOMAIN)
            generator_of_generators = generate_ids_map()
            for generator in generator_of_generators:
                products_generator = asyncio.run(
                    self.get_products_by_ids(
                        range_of_product_ids=generator,
                        single_product_by_id_url=self.SINGLE_PRODUCT_BY_ID,
                    )
                )
                for product_data in products_generator:
                    if product_data:
                        if isinstance(product_data, dict):
                            if "ins" in product_data.get("data").get("sku"):
                                self.logger.info(
                                    f'Found wrong SKU:{product_data.get("data").get("sku")}. Passing...'  # noqa
                                )
                                pass
                            elif "enc" in product_data.get("data").get("sku"):
                                self.logger.info(
                                    f'Found wrong SKU:{product_data.get("data").get("sku")}. Passing...'  # noqa
                                )
                                pass
                            else:
                                data = product_data_extract(
                                    product_response=product_data
                                )
                                api_update_or_create_product(
                                    name=data.get("name"),
                                    url=data.get("url"),
                                    type_id=data.get("type_id"),
                                    scraped_id=data.get("scraped_id"),
                                    api_url=data.get("api_url"),
                                    short_description=data.get(
                                        "short_description"
                                    ),  # noqa
                                    sku=data.get("sku"),
                                    ean=data.get("ean"),
                                    brand_name=data.get("brand_name"),
                                    promotion=data.get("promotion"),
                                    default_price=data.get("default_price"),
                                    promo_price=data.get("promo_price"),
                                    unit_type=data.get("unit_type"),
                                    conversion=data.get("conversion"),
                                    conversion_unit=data.get("conversion_unit"),  # noqa
                                    qty_per_package=data.get("qty_per_package"),  # noqa
                                    tax_rate=data.get("tax_rate"),
                                    parrent_category_from_path=data.get(
                                        "parrent_category_from_path"
                                    ),
                                    parrent_eccomerce_store=parrent_e_store,
                                    last_scrape=data.get("last_scrape"),
                                )
                        else:
                            self.logger.error(
                                f"Received wrong response type: {product_data}"
                            )
                            pass
                    else:
                        self.logger.error(
                            "Received no response for Product URL..."
                        )  # noqa
                        pass
        except EccommerceStore.DoesNotExist:
            self.logger.error("No parrent EccommerceStore found. Quiting...")
            pass

    @calculate_time
    def scrape_product_local_data(self):
        """
        Scrape ProductLocalData for current active LocalStores.
        """

        active_local_stores_ids = self.generate_active_local_stores_ids()
        product_ids_list = self.generate_list_of_products_ids_list()

        for store_id in active_local_stores_ids:
            for ids_list in product_ids_list:
                product_local_data_feature = asyncio.run(
                    self.get_products_by_ids_for_local_store(
                        store_id=store_id,
                        single_product_by_id_for_store_id_url=self.SINGLE_PRODUCT_BY_ID_FOR_STORE_ID,  # noqa
                        iterator_of_product_ids=ids_list,
                    )
                )
                for product_local_data in product_local_data_feature:
                    if product_local_data:
                        if isinstance(product_local_data, dict):
                            try:
                                data = product_local_data_extract(
                                    product_store_response=product_local_data
                                )
                                parrent_product = Product.objects.get(
                                    scraped_id=data.get("product_id")
                                )
                                parrent_local_store = LocalStore.objects.get(
                                    scraped_id=data.get("local_store_id")
                                )
                                api_update_or_create_product_local_data(
                                    parrent_product=parrent_product,
                                    parrent_product_scraped_id=parrent_product.scraped_id,  # noqa
                                    local_store_name=parrent_local_store.name,
                                    local_store_scraped_id=parrent_local_store.scraped_id,  # noqa
                                    name=data.get("name"),
                                    price=data.get("price"),
                                    type_id=data.get("type"),
                                    quantity=data.get("quantity"),
                                    stock_status=data.get("stock_status"),
                                    availability=data.get("availability"),
                                    last_scrape=data.get("last_scrape"),
                                )
                            except Exception as e:
                                self.logger.error(
                                    f"(scrape_product_local_data) Some other exception: {e}"  # noqa
                                )
                                raise
                        else:
                            self.logger.error(
                                f"Received wrong response type: {product_local_data}"  # noqa
                            )
                            pass
                    else:
                        self.logger.error(
                            "Received no response for ProductLocalData URL..."
                        )
                        pass

    @calculate_time
    def validate_products_urls(self):
        """
        Validate Product while requesting it's URL.
        Products with OK response are set to active.
        """

        list_of_products_lists = self.generate_list_of_products_urls_list()
        for product_list in list_of_products_lists:
            products_iterator = asyncio.run(
                self.get_products_by_urls(
                    iterator_of_urls=product_list,
                )
            )
            for product_response in products_iterator:
                if product_response:
                    validate_product_active(
                        product_url=product_response[0],
                        response=product_response[1],  # noqa
                    )
