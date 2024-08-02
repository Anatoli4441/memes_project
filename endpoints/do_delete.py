from endpoints.endpoint import Endpoint


class DoDelete(Endpoint):

    def delete_meme(self, meme_id):
        return self.delete(f"/meme/{meme_id}")
