import requests


class MemeClient:
    BASE_URL = "http://167.172.172.115:52355"

    def __init__(self, token):
        self.token = token

    def _headers(self):
        return {"Authorization": self.token}

    def get_memes(self):
        response = requests.get(f"{self.BASE_URL}/meme", headers=self._headers())
        response.raise_for_status()
        return response.json()["data"]

    def get_meme(self, meme_id):
        response = requests.get(f"{self.BASE_URL}/meme/{meme_id}", headers=self._headers())
        response.raise_for_status()
        return response.json()

    def create_meme(self, text, url, tags, info):
        payload = {"text": text, "url": url, "tags": tags, "info": info}
        response = requests.post(f"{self.BASE_URL}/meme", headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def update_meme(self, meme_id, text, url, tags, info):
        payload = {"id": meme_id, "text": text, "url": url, "tags": tags, "info": info}
        response = requests.put(f"{self.BASE_URL}/meme/{meme_id}", headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def delete_meme(self, meme_id):
        response = requests.delete(f"{self.BASE_URL}/meme/{meme_id}", headers=self._headers())
        response.raise_for_status()
        return response.text
