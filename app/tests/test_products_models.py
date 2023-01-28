"""
Tests for Products models.
"""
import pytest
from products import models


pytestmark = pytest.mark.django_db


class TestProductsModels:
    """Test cases for products app models."""

    def test_create_product_successful(
        self, example_category, example_eccommerce_store
    ):
        """Test creating Product object is successful."""

        e_store = example_eccommerce_store
        category = example_category
        assert models.Product.objects.all().count() == 0
        product = models.Product.objects.create(
            name="Test Product",
            url="http://example.com/test-product-1",
            parrent_store=e_store,
            parrent_category=category,
        )
        assert models.Product.objects.all().count() == 1
        assert isinstance(product, models.Product) is True

    def test_product_str_method(self, example_product):
        """Test that __str__ for Product is properly generated."""

        product = example_product
        assert str(product) == product.name

    def test_create_product_local_data_successful(
        self,
        example_product,
        example_local_store,
    ):
        """Test creating ProductLocalData object is successful."""

        product = example_product
        local_store = example_local_store
        assert models.ProductLocalData.objects.all().count() == 0
        product_local_data = models.ProductLocalData.objects.create(
            parrent_product=product,
            parrent_local_store=local_store,
            name="Test Product",
        )
        assert models.ProductLocalData.objects.all().count() == 1
        assert isinstance(product_local_data, models.ProductLocalData) is True

    def test_product_local_data_str_method(self, example_product_local_data):
        """Test that __str__ is properly generated."""

        product_local_data = example_product_local_data
        assert (
            str(product_local_data)
            == f"{product_local_data.parrent_local_store.name}: {product_local_data.name}"  # noqa
        )

    def test_create_product_extra_field_successful(self, example_product):
        """Test creating ProductExtraField is successful."""

        product = example_product
        assert models.ProductExtraField.objects.all().count() == 0
        product_extra_field = models.ProductExtraField.objects.create(
            parrent_product=product,
            field_name="Test Field",
            field_data="Test Field Data...",
        )
        assert models.ProductExtraField.objects.all().count() == 1
        assert isinstance(product_extra_field, models.ProductExtraField) is True  # noqa

    def test_product_extra_field_str_method(self, example_product_extra_field):
        """Test that __str__ is properly generated for ProductExtraField."""

        product_extra_field = example_product_extra_field
        assert (
            str(product_extra_field)
            == f"{product_extra_field.parrent_product.name}: {product_extra_field.field_name}"  # noqa
        )
