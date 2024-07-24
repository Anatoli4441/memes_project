import allure
import pytest
import requests


@allure.feature('Meme API')
@allure.story('Get Memes')
def test_get_memes(meme_client):
    with allure.step("Retrieve list of memes"):
        response = meme_client.get_memes()
        assert isinstance(response, list), "Response should be a list of memes"


@allure.feature('Meme API')
@allure.story('Create Meme')
def test_create_meme(meme_client):
    with allure.step("Create a new meme"):
        meme = meme_client.create_meme(
            "Zoning Out Black Cat",
            "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            ["black", "cat"],
            {"colours": ["black", "red"]}
        )

        expected = {
            "text": "Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }

        assert all(
            meme.get(key) == value for key, value in expected.items()), "Meme attributes did not match expected values"


@allure.feature('Meme API')
@allure.story('Create Meme Without URL')
def test_create_meme_without_url(meme_client):
    with allure.step("Attempt to create a meme without a URL"):
        response = requests.post(
            f"{meme_client.BASE_URL}/meme",
            headers=meme_client._headers(),
            json={
                "text": "Zoning Out Black Cat",
                "tags": ["black", "cat"],
                "info": {"colours": ["black", "red"]}
            }
        )
        assert response.status_code == 400, "Expected HTTP 400 Bad Request status code"


@allure.feature('Meme API')
@allure.story('Get Meme by ID')
def test_get_meme(meme_client, created_meme):
    with allure.step("Retrieve a specific meme by ID"):
        fetched_meme = meme_client.get_meme(created_meme["id"])
        expected = {
            "id": created_meme["id"],
            "text": created_meme["text"],
            "url": created_meme["url"],
            "tags": created_meme["tags"],
            "info": created_meme["info"]
        }
        assert all(fetched_meme.get(key) == value for key, value in
                   expected.items()), "Fetched meme attributes did not match expected values"


@allure.feature('Meme API')
@allure.story('Get Meme with Wrong ID')
def test_get_meme_with_wrong_id(meme_client):
    with allure.step("Retrieve a meme with a non-existent ID"):
        non_existent_id = "non_existent_id_12345"
        response = requests.get(
            f"{meme_client.BASE_URL}/meme/{non_existent_id}",
            headers=meme_client._headers()
        )
        assert response.status_code == 404, "Expected HTTP 404 Not Found status code"


@allure.feature('Meme API')
@allure.story('Update Meme')
def test_update_meme(meme_client, created_meme):
    with allure.step("Update an existing meme"):
        updated_meme = meme_client.update_meme(
            created_meme["id"],
            "I like the meme named Zoning Out Black Cat",
            "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            ["black", "cat", "green eyes"],
            {"colours": ["black", "red", "green"]}
        )

        expected = {
            "text": "I like the meme named Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }

        assert all(updated_meme.get(key) == value for key, value in
                   expected.items()), "Updated meme attributes did not match expected values"


@allure.feature('Meme API')
@allure.story('Wrong Update Meme')
def test_wrong_update_meme(meme_client, created_meme):
    with allure.step("Attempt to update a meme with missing arguments"):
        with pytest.raises(TypeError) as excinfo:
            meme_client.update_meme(created_meme["id"])
        assert "missing 4 required positional arguments: 'text', 'url', 'tags', and 'info'" in str(excinfo.value)


@allure.feature('Meme API')
@allure.story('Delete Meme')
def test_delete_meme(meme_client, created_meme):
    with allure.step("Delete an existing meme"):
        response = meme_client.delete_meme(created_meme["id"])
        assert "successfully deleted" in response
