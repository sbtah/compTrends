from products.models import Product, ProductLocalData, ProductExtraField
from categories.models import Category
from utilites.logger import logger
from django.db.models import Q
import datetime


def api_update_or_create_product(
    name,
    url,
    scraped_id,
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
    parrent_local_store,
    name,
    price,
    quantity,
    stock_status,
    availability,
    last_scrape,
):
    try:
        # Poll.objects.get(Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
        product_local_data = ProductLocalData.objects.get(
            Q(parrent_local_store=parrent_local_store)
            & Q(parrent_product=parrent_product)
            & Q(last_scrape=last_scrape)
        )
    except ProductLocalData.DoesNotExist:
        pass
