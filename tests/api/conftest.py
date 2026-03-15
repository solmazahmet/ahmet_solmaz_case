import pytest
from config.config import PETSTORE_BASE_URL


@pytest.fixture
def base_url():
    return PETSTORE_BASE_URL
