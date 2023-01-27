"""
Tests for Stores models.
"""
import pytest
from stores import models


pytestmark = pytest.mark.django_db


class TestStoreModels:
    """Test cases for all stores app models."""

    def test_create_eccommerce_store(self):
        """Test creating EccommerceStore is successful."""

        assert models.EccommerceStore.objects.all().count() == 0
        e_store = models.EccommerceStore.objects.create(
            domain="teststore.com",
            main_url="https://teststore.com/",
            module_name="test_store",
            class_name="TestStore",
        )
        assert models.EccommerceStore.objects.all().count() == 1
        assert isinstance(e_store, models.EccommerceStore) is True

    def test_eccommerce_store_str_method(self, example_eccommerce_store):
        """Test that __str__ is properly generated."""

        e_store = example_eccommerce_store
        assert str(e_store) == e_store.domain
