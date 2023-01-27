from django.db import models


class Category(models.Model):
    """Category object."""

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, unique=True)

    scraped_id = models.IntegerField(null=True)
    meta_title = models.CharField(max_length=255, blank=True)
    category_path = models.CharField(max_length=50, blank=True)
    category_level = models.IntegerField(null=True)
    children_category_count = models.IntegerField(null=True)
    product_count = models.IntegerField(null=True)
    parrent_category = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_scrape = models.DateTimeField(blank=True)

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

    def __str__(self):
        return self.field_name
