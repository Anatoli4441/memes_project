from endpoints.endpoint import Endpoint


class DoPost(Endpoint):

    def add_meme(self, data):
        return self.post("/meme", data)
