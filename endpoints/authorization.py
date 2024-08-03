from endpoints.endpoint import Endpoint


class Authorization(Endpoint):

    def authorize(self, name):
        return self.post("/authorize", {"name": name})

    def check_token(self, token):
        return self.get(f"/authorize/{token}")
