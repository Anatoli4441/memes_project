from endpoints.endpoint import Endpoint


class DoPut(Endpoint):

    def update_meme(self, meme_id, data):
        return self.put(f"/meme/{meme_id}", data)
