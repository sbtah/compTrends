from utilities.logger import logger
from categories.models import Category


def api_update_or_create_category(
    parrent_eccomerce_store,
    name,
    url,
    api_url,
    scraped_id,
    meta_title,
    category_path,
    category_level,
    children_category_count,
    product_count,
    last_scrape,
):
    """Update or create Category object with data from API call."""
    try:
        category = Category.objects.get(scraped_id=scraped_id)
        category.name = name
        category.url = url
        category.api_url = api_url
        category.meta_title = meta_title
        category.category_path = category_path
        category.category_level = category_level
        category.children_category_count = children_category_count
        category.product_count = product_count
        category.last_scrape = last_scrape
        category.parrent_store = parrent_eccomerce_store
        category.save()
        logger.info(f"Updated Category: {category}")
    except Category.DoesNotExist:
        category = Category.objects.create(
            name=name,
            url=url,
            api_url=api_url,
            scraped_id=scraped_id,
            meta_title=meta_title,
            category_path=category_path,
            category_level=category_level,
            children_category_count=children_category_count,
            product_count=product_count,
            parrent_store=parrent_eccomerce_store,
            last_scrape=last_scrape,
        )
        logger.info(f"Created Category: {category}")
    return category
