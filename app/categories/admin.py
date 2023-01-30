from django.contrib import admin
from categories import models


class CategoryAdmin(admin.ModelAdmin):
    """Custom admin for Category object."""

    list_filter = (
        "name",
        "scraped_id",
        "category_level",
        "is_active",
        "last_scrape",
    )
    list_display = (
        "name",
        "scraped_id",
        "category_level",
        "is_active",
        "last_scrape",
    )
    search_fields = [
        "name",
        "scraped_id",
        "category_level",
        "is_active",
        "last_scrape",
    ]


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.CategoryExtraField)
