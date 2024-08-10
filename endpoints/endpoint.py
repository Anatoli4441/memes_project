import requests


class Endpoint:
    BASE_URL = "http://167.172.172.115:52355"

    def __init__(self, token=None):
        self.token = token
        self.response = None  # Свойство для хранения последнего ответа

    def _headers(self):
        if self.token:
            return {'Authorization': self.token}
        return {}

    def post(self, path, data):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        self.response = requests.post(url, json=data, headers=headers)
        return self.response

    def get(self, path):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        self.response = requests.get(url, headers=headers)
        return self.response

    def put(self, path, data):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        self.response = requests.put(url, json=data, headers=headers)
        return self.response

    def delete(self, path):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        self.response = requests.delete(url, headers=headers)
        return self.response

    def check_status_code(self, expected_status):
        assert self.response.status_code == expected_status

    def check_meme_data(self, expected_data):
        meme = self.response.json()
        assert meme["text"] == expected_data["text"]
        assert meme["url"] == expected_data["url"]
        assert meme["tags"] == expected_data["tags"]
        assert meme["info"] == expected_data["info"]
