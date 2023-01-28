from django.db import models
from stores.models import EccommerceStore


class Category(models.Model):
    """Category object."""

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, unique=True)

    api_url = models.URLField(max_length=255, blank=True)
    scraped_id = models.IntegerField(null=True)
    meta_title = models.CharField(max_length=255, blank=True)
    category_path = models.CharField(max_length=50, blank=True)
    category_level = models.IntegerField(null=True)
    children_category_count = models.IntegerField(null=True)
    product_count = models.IntegerField(null=True)
    parrent_store = models.ForeignKey(
        EccommerceStore,
        on_delete=models.CASCADE,
    )
    parrent_category = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True
    )
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class CategoryExtraField(models.Model):
    """
    Extra field for Category object,
    used if we want to extend model with extra data.
    """

    parrent_category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    field_name = models.CharField(max_length=100)
    field_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.field_name
