"""
Tests for Stores models.
"""
import pytest
from stores import models


pytestmark = pytest.mark.django_db


class TestStoresModels:
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

    def test_create_local_store(self, example_eccommerce_store):
        """Test creating LocalStore is successful."""

        e_store = example_eccommerce_store

        assert models.LocalStore.objects.all().count() == 0
        local_store = models.LocalStore.objects.create(
            parrent_store=e_store,
            name="Local Store 1",
            scraped_id=1,
            is_active=True,
        )
        assert models.LocalStore.objects.all().count() == 1
        assert isinstance(local_store, models.LocalStore) is True

    def test_local_store_str_method(self, example_local_store):
        """Test that __str__ is properly generated for LocalStore."""

        local_store = example_local_store
        assert str(local_store) == f"{local_store.scraped_id}: {local_store.name}"

    def test_create_store_extra_field(self, example_eccommerce_store):
        """Test creating StoreExtraField object."""

        e_store = example_eccommerce_store
        assert models.StoreExtraField.objects.all().count() == 0
        store_extra_field = models.StoreExtraField.objects.create(
            parrent_store=e_store,
            field_name="Extra Field",
            field_data="Some extra data...",
        )
        assert models.StoreExtraField.objects.all().count() == 1
        assert isinstance(store_extra_field, models.StoreExtraField) is True
