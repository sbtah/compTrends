"""
Tests for Categories models.
"""
import pytest
from categories import models


pytestmark = pytest.mark.django_db


class TestCategoriesModels:
    """Test cases for all categories app models."""

    def test_create_category_successful(self, example_eccommerce_store):
        """Test creating Category object is successful."""

        e_store = example_eccommerce_store
        assert models.Category.objects.all().count() == 0
        category = models.Category.objects.create(
            name="Test Category",
            url="http://example-store.com/test-category/",
            parrent_store=e_store,
            category_path="1/2/1574/1839/7251/4255",
        )
        assert models.Category.objects.all().count() == 1
        assert isinstance(category, models.Category) is True

    def test_category_str_method(self, example_category):
        """Test that __str__ is properly generated for Category object."""

        category = example_category
        assert str(category) == category.name

    def test_category_pre_save_signal(self, example_category):
        """
        Test that save method properly saves parrent_category_from_path field.
        """
        category = example_category
        assert category.parrent_category_from_path == int(
            category.category_path.split("/")[-2]
        )

    def test_create_category_extra_field_successful(self, example_category):
        """Test creating CategoryExtraField object is successful."""

        category = example_category
        assert models.CategoryExtraField.objects.all().count() == 0
        category_extra_field = models.CategoryExtraField.objects.create(
            parrent_category=category,
            field_name="Test Field",
            field_data="Some Test Data...",
        )
        assert models.CategoryExtraField.objects.all().count() == 1
        assert (
            isinstance(category_extra_field, models.CategoryExtraField) is True
        )  # noqa
