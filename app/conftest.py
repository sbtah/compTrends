import pytest
from stores.models import EccommerceStore


@pytest.fixture
def example_eccommerce_store():
    return EccommerceStore.objects.create(
        domain="teststore.com",
        main_url="https://teststore.com/",
        module_name="test_store",
        class_name="TestStore",
    )
