import pytest
from stores.models import EccommerceStore, LocalStore


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
