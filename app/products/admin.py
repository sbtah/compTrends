from django.contrib import admin
from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_filter = (
        "is_active",
        "parrent_category",
    )
    list_display = (
        "name",
        "scraped_id",
        "parrent_category",
        "sku",
        "ean",
        "brand_name",
    )
    search_fields = [
        "name",
        "scraped_id",
        "parrent_category__name",
        "sku",
        "ean",
        "brand_name",
    ]


admin.site.register(Product, ProductAdmin)
