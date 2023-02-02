from stores.models import LocalStore
from utilites.logger import logger


def api_update_or_create_local_store(
    parrent_eccomerce_store,
    name,
    scraped_id,
    last_scrape,
):
    """Update or create LocalStore object with data from API call."""

    try:
        local_store = LocalStore.objects.get(scraped_id=scraped_id)
        local_store.name = name
        local_store.last_scrape = last_scrape
        local_store.save()
        logger.info(f"Updated LocalStore: {local_store}")
    except LocalStore.DoesNotExist:
        local_store = LocalStore.objects.create(
            parrent_store=parrent_eccomerce_store,
            name=name,
            scraped_id=scraped_id,
            last_scrape=last_scrape,
        )
        logger.info(f"Created LocalStore: {local_store}")
    return local_store
