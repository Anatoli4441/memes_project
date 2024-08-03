import requests


class Endpoint:
    BASE_URL = "http://167.172.172.115:52355"

    def __init__(self, token=None):
        self.token = token

    def _headers(self):
        if self.token:
            return {'Authorization': self.token}
        return {}

    def post(self, path, data):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        response = requests.post(url, json=data, headers=headers)
        return response

    def get(self, path):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        response = requests.get(url, headers=headers)
        return response

    def put(self, path, data):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        response = requests.put(url, json=data, headers=headers)
        return response

    def delete(self, path):
        url = f"{self.BASE_URL}{path}"
        headers = self._headers()
        response = requests.delete(url, headers=headers)
        return response
