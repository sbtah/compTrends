from utilites.logger import logger
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
    pass

    try:
        category = Category.objects.get(scraped_id=scraped_id)
        if category.name != name:
            category.name = name
            logger.info(f"Updating (name) for: {category} with {name}")
        if category.url != url:
            category.url = url
            logger.info(f"Updating (url) for: {category} with {url}")
        if category.api_url != api_url:
            category.api_url = api_url
            logger.info(f"Updating (api_url) for: {category} with {api_url}")
        if category.meta_title != meta_title:
            category.meta_title = meta_title
            logger.info(
                f"Updating (meta_title) for: {category} with {meta_title}",
            )
        if category.category_path != category_path:
            category.category_path = category_path
            logger.info(
                f"Updating (category_path) for: {category} with {category_path}",
            )
        if category.category_level != category_level:
            category.category_level = category_level
            logger.info(
                f"Updating (category_level) for: {category} with {category_level}"  # noqa
            )
        if category.children_category_count != children_category_count:
            category.children_category_count = children_category_count
            logger.info(
                f"Updating (children_category_count) for: {category} with {children_category_count}"  # noqa
            )
        if category.product_count != product_count:
            category.product_count = product_count
            logger.info(
                f"Updating (product_count) for: {category} with {product_count}"  # noqa
            )
        category.last_scrape = last_scrape
        logger.info(
            f"Updating (last_scrape) for: {category} with {last_scrape}"  # noqa
        )
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
