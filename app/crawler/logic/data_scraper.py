from datetime import date

from crawler.helpers.time_it import calculate_time
from crawler.logic.api_crawler import ApiCrawler
from crawler.options.endpoints import LOCAL_STORES_ENDPOINT
from stores.builders import api_update_or_create_local_store
from stores.models import EccommerceStore


class DataApiScraper(ApiCrawler):
    """
    Scrapes data from specified API Endpoints.
    """

    LOCAL_STORES_ENDPOINT = LOCAL_STORES_ENDPOINT

    def __init__(self, domain, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.domain = domain

    @calculate_time
    def scrape_local_stores(self):
        """
        Discover LocalStores by requesting Local Stores endpoint.
        """
        try:
            parrent_e_store = EccommerceStore.objects.get(domain=self.domain)
        except EccommerceStore.DoesNotExist:
            self.logger.error("No EccomerceStore found. Creating...")
            parrent_e_store = EccommerceStore.objects.create(
                domain=self.domain, main_url=f"http://{self.domain}/"
            )
        finally:
            stores = self.get_local_stores(
                local_stores_endpoint=self.LOCAL_STORES_ENDPOINT
            )
            if stores:
                for store in stores:
                    store_name = store.get("name")
                    store_id = store.get("selected_shop_store_view")
                    last_scraped = date.today()
                    api_update_or_create_local_store(
                        parrent_eccomerce_store=parrent_e_store,
                        name=store_name,
                        scraped_id=store_id,
                        last_scrape=last_scraped,
                    )
            else:
                self.logger.error(f"Failed requesting URL: {LOCAL_STORES_ENDPOINT}")
                pass
