from endpoints.endpoint import Endpoint


class TestMemeAPI:

    def test_authorization(self, authorization):
        response = authorization.authorize("Anatoliy")
        Endpoint.check_status_code(response, 200)

    def test_valid_token(self, do_get, token):
        response = do_get.check_token(token)
        Endpoint.check_status_code(response, 200)

    def test_get_all_memes(self, do_get):
        response = do_get.get_all_memes()
        Endpoint.check_status_code(response, 200)

    def test_get_meme_by_id(self, meme, do_get, meme_data):
        meme_id = meme["id"]
        response = do_get.get_meme_by_id(meme_id)
        Endpoint.check_status_code(response, 200)
        Endpoint.check_meme_data(response.json(), meme_data)

    def test_add_meme(self, meme, meme_data):
        Endpoint.check_meme_data(meme, meme_data)

    def test_update_meme(self, meme, do_put, do_get):
        meme_id = meme["id"]
        updated_data = {
            "id": meme_id,
            "text": "I like the meme named Zoning Out Black Cat",
            "url": meme["url"],
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        response = do_put.update_meme(meme_id, updated_data)
        Endpoint.check_status_code(response, 200)

        response = do_get.get_meme_by_id(meme_id)
        Endpoint.check_status_code(response, 200)
        Endpoint.check_meme_data(response.json(), updated_data)

    def test_delete_meme(self, meme, do_delete, do_get):
        meme_id = meme["id"]

        response = do_delete.delete_meme(meme_id)
        Endpoint.check_status_code(response, 200)

        response = do_get.get_meme_by_id(meme_id)
        Endpoint.check_status_code(response, 404)

    def test_invalid_token(self, do_get):
        response = do_get.check_token("xsdsd232333")
        Endpoint.check_status_code(response, 404)

    def test_nonexistent_meme(self, do_get):
        response = do_get.get_meme_by_id("3234348949493x")
        Endpoint.check_status_code(response, 404)

    def test_add_meme_without_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        Endpoint.check_status_code(response, 400)

    def test_update_meme_with_nonexistent_id(self, do_put):
        data = {
            "id": "3234348949493x",
            "text": "I like the meme named Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        response = do_put.update_meme("3234348949493x", data)
        Endpoint.check_status_code(response, 404)

    def test_delete_meme_created_by_other_user(self, do_delete, other_user_meme):
        meme_id = other_user_meme["id"]
        response = do_delete.delete_meme(meme_id)
        Endpoint.check_status_code(response, 403)

    def test_add_meme_with_int_in_text(self, do_post):
        data = {
            "text": 3,
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        Endpoint.check_status_code(response, 400)

    def test_add_meme_with_int_in_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "url": 3,
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        Endpoint.check_status_code(response, 400)

    def test_unauthorized_access_get(self, unauthorized_do_get):
        response = unauthorized_do_get.get_all_memes()
        Endpoint.check_status_code(response, 401)

    def test_unauthorized_access_post(self, unauthorized_do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = unauthorized_do_post.add_meme(data)
        Endpoint.check_status_code(response, 401)

    def test_unauthorized_access_put(self, unauthorized_do_put, anatoliy_memes):
        meme_to_update = next((m for m in anatoliy_memes), None)
        assert meme_to_update is not None, "No meme found created by Anatoliy"

        updated_data = {
            "id": meme_to_update["id"],
            "text": "I like the meme named Zoning Out Black Cat",
            "url": meme_to_update["url"],
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        response = unauthorized_do_put.update_meme(meme_to_update["id"], updated_data)
        Endpoint.check_status_code(response, 401)

    def test_unauthorized_access_delete(self, unauthorized_do_delete, anatoliy_memes):
        meme_to_delete = next((m for m in anatoliy_memes), None)
        assert meme_to_delete is not None, "No meme found created by Anatoliy"

        response = unauthorized_do_delete.delete_meme(meme_to_delete["id"])
        Endpoint.check_status_code(response, 401)
