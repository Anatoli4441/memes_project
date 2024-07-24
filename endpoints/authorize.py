import requests


class AuthorizeClient:
    BASE_URL = "http://167.172.172.115:52355"

    def __init__(self):
        self.token = None

    def authorize(self, name):
        response = requests.post(f"{self.BASE_URL}/authorize", json={"name": name})
        response.raise_for_status()
        self.token = response.json().get("token")
        return self.token

    def check_token(self):
        if not self.token:
            raise RuntimeError("Token not found. Please authorize first.")
        headers = {"Authorization": self.token}
        response = requests.get(f"{self.BASE_URL}/authorize/{self.token}", headers=headers)
        response.raise_for_status()
        return response.text
