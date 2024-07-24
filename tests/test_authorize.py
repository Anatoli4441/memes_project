import allure
import requests


@allure.feature('Authorization API')
@allure.story('Authorize')
def test_authorize(authorize_client):
    with allure.step("Authorize user"):
        token = authorize_client.authorize("Anatoliy")
        assert token, "Authorization token should not be None"


@allure.feature('Authorization API')
@allure.story('Check Token')
def test_check_token(authorize_client):
    with allure.step("Check if token is valid"):
        authorize_client.authorize("Anatoliy")
        response = authorize_client.check_token()
        assert "Token is alive" in response


@allure.feature('Authorization API')
@allure.story('Invalid Token')
def test_check_token_with_invalid_token(authorize_client):
    with allure.step("Check token validity with invalid token"):
        invalid_token = "invalid_token_12345"
        headers = {"Authorization": f"Bearer {invalid_token}"}
        response = requests.get(f"{authorize_client.BASE_URL}/{invalid_token}", headers=headers)
        assert response.status_code == 404, "Expected HTTP 404 NOT FOUND"
