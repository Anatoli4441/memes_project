from endpoints.endpoint import Endpoint


class DoGet(Endpoint):

    def get_all_memes(self):
        return self.get("/meme")

    def get_meme_by_id(self, meme_id):
        return self.get(f"/meme/{meme_id}")

    def check_token(self, token):
        return self.get(f"/authorize/{token}")
