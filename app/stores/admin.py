from django.contrib import admin
from stores import models


class LocalStoreAdmin(admin.ModelAdmin):
    """Custom admin for LocalStore object."""

    list_filter = ("name", "is_active")
    list_display = ("name", "scraped_id", "is_active")
    search_fields = ["name"]


admin.site.register(models.EccommerceStore)
admin.site.register(models.LocalStore, LocalStoreAdmin)
admin.site.register(models.StoreExtraField)
