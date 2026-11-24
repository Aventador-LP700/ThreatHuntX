import pytest
from app.catalog import Catalog
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def catalog():
    return Catalog()


@pytest.fixture
def client(tmp_path, catalog):
    with TestClient(create_app(tmp_path / "fixture.sqlite", catalog)) as test_client:
        yield test_client
