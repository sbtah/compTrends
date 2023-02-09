from django.contrib import admin
from products.models import Product, ProductLocalData


class IsNullFilter(admin.SimpleListFilter):
    title = "No Local Data"
    parameter_name = "LocalData"

    def lookups(self, request, model_admin):
        return (("None", ("Product without LocalData")),)

    def queryset(self, request, queryset):
        if self.value() == "None":
            return queryset.filter(
                productlocaldata__isnull=True,
            )


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = (
        "name",
        "url",
        "scraped_id",
        "type_id",
        "api_url",
        "short_description",
        "sku",
        "ean",
        "brand_name",
        "promotion",
        "default_price",
        "promo_price",
        "unit_type",
        "conversion",
        "conversion_unit",
        "qty_per_package",
        "tax_rate",
        "parrent_category_from_path",
        "parrent_store",
        "parrent_category",
        "last_scrape",
    )
    ordering = ("-is_active",)
    list_filter = (
        IsNullFilter,
        "is_active",
        "parrent_category",
    )
    list_display = (
        "name",
        "scraped_id",
        "parrent_category",
        "is_active",
        "promotion",
        "sku",
        "ean",
        "brand_name",
    )
    search_help_text = (
        "Search Products by: name, scraped_id, sku, ean or name of parrent Category."
    )
    search_fields = [
        "name",
        "scraped_id",
        "parrent_category__name",
        "sku",
        "ean",
        "brand_name",
    ]


class ProductLocalDataAdmin(admin.ModelAdmin):
    readonly_fields = (
        "parrent_product",
        "parrent_product_scraped_id",
        "local_store_name",
        "local_store_scraped_id",
        "name",
        "price",
        "type_id",
        "quantity",
        "stock_status",
        "availability",
        "last_scrape",
    )
    list_filter = ("local_store_name",)
    autocomplete_fields = ("parrent_product",)
    list_display = (
        "pk",
        "name",
        "parrent_product_scraped_id",
        "local_store_name",
        "price",
        "quantity",
        "stock_status",
        "availability",
        "last_scrape",
    )
    search_help_text = (
        "Search ProductLocalData by: name, name of Store or scraped_id of Store."
    )
    search_fields = [
        "name",
        "local_store_name",
        "local_store_scraped_id",
        "parrent_product_scraped_id",
        "parrent_product__name",
    ]
    list_select_related = ["parrent_product"]


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductLocalData, ProductLocalDataAdmin)
admin.site.site_header = "compTrends"
