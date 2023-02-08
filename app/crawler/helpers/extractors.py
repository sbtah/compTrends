from crawler.options.endpoints import SINGLE_PRODUCT_BY_ID
from datetime import date


def local_store_data_extract(store_response):
    """
    Extract and clean LocalStore data. Returns data ready to be saved.
    """
    store_name = store_response.get("name")
    store_id = store_response.get("selected_shop_store_view")
    last_scrape = date.today()
    return {
        "store_name": store_name,
        "store_id": store_id,
        "last_scrape": last_scrape,
    }


def category_data_extract(category_response):
    """
    Extract and clean Category data. Returns data ready to be saved to database.
    """
    name = category_response.get("name")
    url = category_response.get("url")
    scraped_id = category_response.get("id")
    api_url = SINGLE_PRODUCT_BY_ID.format(scraped_id)
    meta_title = (
        ""
        if category_response.get("meta_title") is None
        else category_response.get("meta_title")
    )
    category_path = category_response.get("path")
    category_level = category_response.get("level")
    children_category_count = category_response.get("children_count")
    product_count = category_response.get("product_count")
    last_scrape = date.today()
    return {
        "name": name,
        "url": url,
        "scraped_id": scraped_id,
        "api_url": api_url,
        "meta_title": meta_title,
        "category_path": category_path,
        "category_level": category_level,
        "children_category_count": children_category_count,
        "product_count": product_count,
        "last_scrape": last_scrape,
    }


def product_data_extract(product_response):
    """
    Extract and clean Product data. Returns data ready to be saved to database.
    """
    name = product_response.get("data").get("name")
    url = product_response.get("data").get("url_path")
    type_id = product_response.get("data").get("type_id")
    scraped_id = product_response.get("data").get("entity_id")
    api_url = SINGLE_PRODUCT_BY_ID.format(scraped_id)
    short_description = (
        ""
        if product_response.get("data").get("short_description") is None
        else product_response.get("data").get("short_description")
    )
    sku = product_response.get("data").get("sku")
    ean = (
        ""
        if product_response.get("data").get("ean") is None
        else product_response.get("data").get("ean")
    )
    brand_name = (
        ""
        if product_response.get("data").get("brand_data").get("name") is None
        else product_response.get("data").get("brand_data").get("name")
    )
    promotion = (
        False
        if product_response.get("data").get("info_boxes").get("promo_price") is None
        else True
    )
    default_price = product_response.get("data").get("default_price")
    promo_price = product_response.get("data").get("promo_price")
    unit_type = product_response.get("data").get("price_unit")
    conversion = (
        ""
        if product_response.get("data").get("conversion") is None
        else product_response.get("data").get("conversion")
    )
    conversion_unit = (
        ""
        if product_response.get("data").get("conversion_unit") is None
        else product_response.get("data").get("conversion_unit")
    )
    qty_per_package = product_response.get("data").get("qty_per_package")
    tax_rate = product_response.get("data").get("tax_rate")
    try:
        parrent_category_from_path = (
            product_response.get("data").get("category_path")[-1].get("id")
        )
    except IndexError:
        parrent_category_from_path = None
    last_scrape = date.today()
    return {
        "name": name,
        "url": url,
        "type_id": type_id,
        "scraped_id": scraped_id,
        "api_url": api_url,
        "short_description": short_description,
        "sku": sku,
        "ean": ean,
        "brand_name": brand_name,
        "promotion": promotion,
        "default_price": default_price,
        "promo_price": promo_price,
        "unit_type": unit_type,
        "conversion": conversion,
        "conversion_unit": conversion_unit,
        "qty_per_package": qty_per_package,
        "tax_rate": tax_rate,
        "parrent_category_from_path": parrent_category_from_path,
        "last_scrape": last_scrape,
    }


def product_local_data_extract(product_store_response):
    """
    Extract and clean ProductLocalData data.
    Returns data ready to be saved to database.
    """
    product_id = list(product_store_response.get("products").keys())[0]
    data = product_store_response.get("products").get(f"{product_id}")
    try:
        local_store_id = data.get("sources")[0].get("id")
    except TypeError:
        local_store_id = product_store_response.get("store")
    name = data.get("name")
    price = data.get("price")
    type = data.get("type")
    quantity = data.get("qty")
    stock_status = data.get("stock_status")
    availability = data.get("availability")
    last_scrape = date.today()
    return {
        "product_id": product_id,
        "local_store_id": local_store_id,
        "name": name,
        "price": price,
        "type": type,
        "quantity": quantity,
        "stock_status": stock_status,
        "availability": availability,
        "last_scrape": last_scrape,
    }
