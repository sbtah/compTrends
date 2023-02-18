from products.models import Product, ProductLocalData, ProductExtraField
from categories.models import Category
from utilities.logger import logger
from django.db.models import Q


def api_update_or_create_product(
    name,
    url,
    scraped_id,
    type_id,
    api_url,
    short_description,
    sku,
    ean,
    brand_name,
    promotion,
    default_price,
    promo_price,
    unit_type,
    conversion,
    conversion_unit,
    qty_per_package,
    tax_rate,
    parrent_category_from_path,
    parrent_eccomerce_store,
    last_scrape,
):
    """Create or update Product object with data from API call."""

    try:
        product = Product.objects.get(scraped_id=scraped_id)
        product.name = name
        product.url = url
        product.type_id = type_id
        product.api_url = api_url
        product.short_description = short_description
        product.sku = sku
        product.ean = ean
        product.brand_name = brand_name
        product.promotion = promotion
        product.default_price = default_price
        product.promo_price = promo_price
        product.unit_type = unit_type
        product.conversion = conversion
        product.conversion_unit = conversion_unit
        product.qty_per_package = qty_per_package
        product.tax_rate = tax_rate
        product.parrent_category_from_path = parrent_category_from_path
        product.last_scrape = last_scrape
        try:
            parrent_cat = Category.objects.get(
                scraped_id=product.parrent_category_from_path
            )
            parrent_cat.product_set.add(product)
        except Category.DoesNotExist:
            logger.error("Parrent Category does not exist. Passing..")
            pass
        finally:
            product.save()
            logger.info(f"Updated Product: {product}")
    except Product.DoesNotExist:
        try:
            parrent_cat = Category.objects.get(scraped_id=parrent_category_from_path)
            product = Product.objects.create(
                name=name,
                url=url,
                scraped_id=scraped_id,
                type_id=type_id,
                api_url=api_url,
                short_description=short_description,
                sku=sku,
                ean=ean,
                brand_name=brand_name,
                promotion=promotion,
                default_price=default_price,
                promo_price=promo_price,
                unit_type=unit_type,
                conversion=conversion,
                conversion_unit=conversion_unit,
                qty_per_package=qty_per_package,
                tax_rate=tax_rate,
                parrent_category_from_path=parrent_category_from_path,
                parrent_store=parrent_eccomerce_store,
                parrent_category=parrent_cat,
                last_scrape=last_scrape,
            )
        except Category.DoesNotExist:
            logger.error(
                f"Parrent Category with ID: {parrent_category_from_path} Not found."
            )
            product = Product.objects.create(
                name=name,
                url=url,
                scraped_id=scraped_id,
                type_id=type_id,
                api_url=api_url,
                short_description=short_description,
                sku=sku,
                ean=ean,
                brand_name=brand_name,
                promotion=promotion,
                default_price=default_price,
                promo_price=promo_price,
                unit_type=unit_type,
                conversion=conversion,
                conversion_unit=conversion_unit,
                qty_per_package=qty_per_package,
                tax_rate=tax_rate,
                parrent_category_from_path=parrent_category_from_path,
                parrent_store=parrent_eccomerce_store,
                last_scrape=last_scrape,
            )
        finally:
            product.save()
            logger.info(f"Created Product: {product}")
    return product


def api_update_or_create_product_local_data(
    parrent_product,
    parrent_product_scraped_id,
    local_store_name,
    local_store_scraped_id,
    name,
    price,
    type_id,
    quantity,
    stock_status,
    availability,
    last_scrape,
):
    try:
        product_local_data = ProductLocalData.objects.get(
            Q(local_store_name=local_store_name)
            & Q(parrent_product=parrent_product)
            & Q(last_scrape=last_scrape)
        )
        product_local_data.parrent_product = parrent_product
        product_local_data.parrent_product_scraped_id = parrent_product_scraped_id
        product_local_data.local_store_name = local_store_name
        product_local_data.local_store_scraped_id = local_store_scraped_id
        product_local_data.name = name
        product_local_data.price = price
        product_local_data.type_id = type_id
        product_local_data.quantity = quantity
        product_local_data.stock_status = stock_status
        product_local_data.availability = availability
        product_local_data.last_scrape = last_scrape
        product_local_data.save()
        logger.info(f"Updated ProductLocalData: {product_local_data}")
    except ProductLocalData.DoesNotExist:
        product_local_data = ProductLocalData.objects.create(
            parrent_product=parrent_product,
            parrent_product_scraped_id=parrent_product_scraped_id,
            local_store_name=local_store_name,
            local_store_scraped_id=local_store_scraped_id,
            name=name,
            price=price,
            type_id=type_id,
            quantity=quantity,
            stock_status=stock_status,
            availability=availability,
            last_scrape=last_scrape,
        )
        logger.info(f"Created ProductLocalData: {product_local_data}")
    return product_local_data


def validate_product_active(product_url, response):
    """
    Validate Product by URL. If response is 200,
        it means that Product is active.
    """
    try:
        product = Product.objects.get(url=product_url)
        if response.status_code == 200:
            product.is_active = True
            product.save()
            logger.info(f"Product: {product} was set to: ACTIVE")
        else:
            product.is_active = False
            product.save()
            logger.info(f"Product: {product} was set to: INACTIVE")
    except Product.DoesNotExist:
        logger.error(f"Cannot find Product with url: {product_url}!")
