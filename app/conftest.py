import pytest
from datetime import date
from stores.models import EccommerceStore, LocalStore
from categories.models import Category
from products.models import Product, ProductLocalData, ProductExtraField


@pytest.fixture
def example_eccommerce_store():
    return EccommerceStore.objects.create(
        domain="teststore.com",
        main_url="https://teststore.com/",
        module_name="test_store",
        class_name="TestStore",
    )


@pytest.fixture
def example_local_store(example_eccommerce_store):
    e_store = example_eccommerce_store
    return LocalStore.objects.create(
        parrent_store=e_store,
        name="Local Store 1",
        scraped_id=1,
        is_active=True,
    )


@pytest.fixture
def example_category(example_eccommerce_store):
    e_store = example_eccommerce_store
    return Category.objects.create(
        name="Test Category",
        url="http://example-store.com/test-category/",
        parrent_store=e_store,
        category_path="1/2/1574/1839/7251/4255",
    )


@pytest.fixture
def example_product(example_category, example_eccommerce_store):
    e_store = example_eccommerce_store
    category = example_category
    return Product.objects.create(
        name="Test Product",
        url="http://example.com/test-product-1",
        parrent_store=e_store,
        parrent_category=category,
        last_scrape=date.today(),
    )


@pytest.fixture
def example_product_local_data(example_product, example_local_store):
    product = example_product
    local_store = example_local_store
    return ProductLocalData.objects.create(
        parrent_product=product,
        parrent_local_store=local_store,
        name="Test Product",
        last_scrape=date.today(),
    )


@pytest.fixture
def example_product_extra_field(example_product):
    product = example_product
    return ProductExtraField.objects.create(
        parrent_product=product,
        field_name="Test Field",
        field_data="Test Field Data...",
    )
