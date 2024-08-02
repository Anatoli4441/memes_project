from endpoints.endpoint import Endpoint


class DoPost(Endpoint):

    def authorize(self, name):
        return self.post("/authorize", {"name": name})

    def add_meme(self, data):
        return self.post("/meme", data)
