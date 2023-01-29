from stores.models import LocalStore
from utilites.logger import logger


def api_update_or_create_local_store(
    parrent_eccomerce_store,
    name,
    scraped_id,
    **kwargs,
):
    """Update or create LocalStore object with data from API call."""

    try:
        local_store = LocalStore.objects.get(scraped_id=scraped_id)
        if local_store.name != name:
            local_store.name = name
            local_store.save()
            logger.info(f"Updated LocalStore: {local_store}")
        else:
            logger.info(f"No Updates for LocalStore: {local_store}. Passing...")
    except LocalStore.DoesNotExist:
        local_store = LocalStore.objects.create(
            parrent_store=parrent_eccomerce_store,
            name=name,
            scraped_id=scraped_id,
            **kwargs,
        )
        logger.info(f"Created LocalStore: {local_store}")
    return local_store
