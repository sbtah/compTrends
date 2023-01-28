from django.db import models
from categories.models import Category
from stores.models import LocalStore


class Product(models.Model):
    """Product object."""

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, unique=True)

    api_url = models.URLField(max_length=255, blank=True)
    scraped_id = models.IntegerField(null=True)
    sku = models.CharField(max_length=50, blank=True)
    ean = models.CharField(max_length=50, blank=True)
    brand_name = models.CharField(max_length=50, blank=True)
    default_price = models.DecimalField(
        blank=True,
        max_digits=7,
        decimal_places=2,
    )
    default_price = models.DecimalField(
        blank=True,
        max_digits=7,
        decimal_places=2,
    )
    unit_type = models.CharField(max_length=10, blank=True)
    conversion = models.CharField(max_length=10, blank=True)
    conversion_unit = models.CharField(max_length=10, blank=True)
    qty_per_package = models.IntegerField(null=True)
    tax_rate = models.CharField(max_length=10, blank=True)
    category_path = models.CharField(max_length=50, blank=True)
    parrent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductLocalData(models.Model):
    """ProductLocalData object."""

    parrent_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    parrent_local_store = models.ForeignKey(
        LocalStore,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        blank=True,
        max_digits=7,
        decimal_places=2,
    )
    quantity = models.IntegerField(null=True)
    stock_status = models.IntegerField(null=True)
    availability = models.CharField(max_length=10, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.parrent_local_store}: {self.name}"


class ProductExtraField(models.Model):
    """
    Extra field for Product object,
    used if we want to extend model with extra data.
    """

    parrent_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    field_name = models.CharField(max_length=100)
    field_data = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_scrape = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.field_name
