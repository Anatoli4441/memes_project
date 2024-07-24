import pytest
from endpoints.authorize import AuthorizeClient
from endpoints.meme import MemeClient
import requests


@pytest.fixture(scope="session")
def authorize_client():
    client = AuthorizeClient()
    client.authorize("Anatoliy")
    return client


@pytest.fixture(scope="session")
def meme_client(authorize_client):
    return MemeClient(authorize_client.token)


@pytest.fixture
def created_meme(meme_client):
    meme = meme_client.create_meme(
        "Test Meme",
        "http://example.com/test_meme.jpg",
        ["test"],
        {"colours": ["blue"]}
    )
    yield meme
    try:
        meme_client.delete_meme(meme["id"])
    except requests.RequestException as e:
        print(f"Failed to delete meme with ID {meme['id']}: {e}")
