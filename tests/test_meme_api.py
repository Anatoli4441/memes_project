

class TestMemeAPI:

    def check_status_code(self, response, expected_status):
        assert response.status_code == expected_status

    def check_meme_data(self, meme, expected_data):
        assert meme["text"] == expected_data["text"]
        assert meme["url"] == expected_data["url"]
        assert meme["tags"] == expected_data["tags"]
        assert meme["info"] == expected_data["info"]

    def test_authorization(self, authorization):
        response = authorization.authorize("Anatoliy")
        self.check_status_code(response, 200)

    def test_valid_token(self, do_get, token):
        response = do_get.check_token(token)
        self.check_status_code(response, 200)

    def test_get_all_memes(self, do_get):
        response = do_get.get_all_memes()
        self.check_status_code(response, 200)

    def test_get_meme_by_id(self, meme, do_get, meme_data):
        meme_id = meme["id"]
        response = do_get.get_meme_by_id(meme_id)
        self.check_status_code(response, 200)
        self.check_meme_data(response.json(), meme_data)

    def test_add_meme(self, meme, meme_data):
        self.check_meme_data(meme, meme_data)

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
        self.check_status_code(response, 200)

        response = do_get.get_meme_by_id(meme_id)
        self.check_status_code(response, 200)
        self.check_meme_data(response.json(), updated_data)

    def test_delete_meme(self, meme, do_delete, do_get):
        meme_id = meme["id"]

        response = do_delete.delete_meme(meme_id)
        self.check_status_code(response, 200)

        response = do_get.get_meme_by_id(meme_id)
        self.check_status_code(response, 404)

    def test_invalid_token(self, do_get):
        response = do_get.check_token("xsdsd232333")
        self.check_status_code(response, 404)

    def test_nonexistent_meme(self, do_get):
        response = do_get.get_meme_by_id("3234348949493x")
        self.check_status_code(response, 404)

    def test_add_meme_without_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        self.check_status_code(response, 400)

    def test_update_meme_with_nonexistent_id(self, do_put):
        data = {
            "id": "3234348949493x",
            "text": "I like the meme named Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        response = do_put.update_meme("3234348949493x", data)
        self.check_status_code(response, 404)

    def test_delete_meme_created_by_other_user(self, do_get, do_delete, meme):
        response = do_get.get_all_memes()
        self.check_status_code(response, 200)

        memes = response.json().get('data', [])
        other_meme = next((m for m in memes if m.get('updated_by') != 'Anatoliy'), None)
        assert other_meme is not None, "No meme found created by another user"

        meme_id = other_meme["id"]
        response = do_delete.delete_meme(meme_id)
        self.check_status_code(response, 403)

    def test_add_meme_with_int_in_text(self, do_post):
        data = {
            "text": 3,
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        self.check_status_code(response, 400)

    def test_add_meme_with_int_in_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "url": 3,  # Неверный тип данных (ожидается строка)
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        self.check_status_code(response, 400)

    def test_unauthorized_access(self, unauthorized_do_get, unauthorized_do_post, unauthorized_do_put, unauthorized_do_delete, anatoliy_memes):
        # Test unauthorized access to each endpoint

        response = unauthorized_do_get.get_all_memes()
        self.check_status_code(response, 401)

        response = unauthorized_do_get.get_all_memes()
        self.check_status_code(response, 401)

        data = {
            "text": "Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = unauthorized_do_post.add_meme(data)
        self.check_status_code(response, 401)

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
        self.check_status_code(response, 401)

        response = unauthorized_do_delete.delete_meme(meme_to_update["id"])
        self.check_status_code(response, 401)
