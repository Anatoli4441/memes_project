class TestMemeAPI:

    def test_authorization(self, do_post):
        response = do_post.authorize("Anatoliy")
        assert response.status_code == 200

    def test_valid_token(self, do_get, token):
        response = do_get.check_token(token)
        assert response.status_code == 200

    def test_get_all_memes(self, do_get):
        response = do_get.get_all_memes()
        assert response.status_code == 200

    def test_get_meme_by_id(self, do_post, do_get, meme_data):
        response = do_post.add_meme(meme_data)
        meme_id = response.json()["id"]

        response = do_get.get_meme_by_id(meme_id)
        assert response.status_code == 200
        assert response.json()["text"] == meme_data["text"]

    def test_add_meme(self, do_post, do_get, meme_data):
        response = do_post.add_meme(meme_data)
        assert response.status_code == 200
        meme_id = response.json()["id"]

        response = do_get.get_meme_by_id(meme_id)
        assert response.status_code == 200
        assert response.json()["text"] == meme_data["text"]

    def test_update_meme(self, do_post, do_put, do_get, meme_data):
        response = do_post.add_meme(meme_data)
        meme_id = response.json()["id"]

        updated_data = {
            "id": meme_id,
            "text": "I like the meme named Zoning Out Black Cat",
            "url": meme_data["url"],
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        response = do_put.update_meme(meme_id, updated_data)
        assert response.status_code == 200

        response = do_get.get_meme_by_id(meme_id)
        assert response.status_code == 200
        assert response.json()["text"] == updated_data["text"]

    def test_delete_meme(self, do_post, do_delete, do_get, meme_data):
        response = do_post.add_meme(meme_data)
        meme_id = response.json()["id"]

        response = do_delete.delete_meme(meme_id)
        assert response.status_code == 200

        response = do_get.get_meme_by_id(meme_id)
        assert response.status_code == 404

    def test_invalid_token(self, do_get):
        response = do_get.check_token("xsdsd232333")
        assert response.status_code == 404

    def test_nonexistent_meme(self, do_get):
        response = do_get.get_meme_by_id("3234348949493x")
        assert response.status_code == 404

    def test_add_meme_without_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        assert response.status_code == 400

    def test_update_meme_with_nonexistent_id(self, do_put):
        data = {
            "id": "3234348949493x",
            "text": "I like the meme named Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        response = do_put.update_meme("3234348949493x", data)
        assert response.status_code == 404

    def test_delete_meme_created_by_other_user(self, do_get, do_delete):
        response = do_get.get_all_memes()
        assert response.status_code == 200

        memes = response.json().get('data', [])

        assert isinstance(memes, list), "Expected list of memes"

        other_meme = next((m for m in memes if m.get('updated_by') != 'Anatoliy'), None)
        assert other_meme is not None, "No meme found created by another user"

        meme_id = other_meme["id"]
        response = do_delete.delete_meme(meme_id)
        assert response.status_code == 403

    def test_add_meme_with_int_in_text(self, do_post):
        data = {
            "text": 3,
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        assert response.status_code == 400

    def test_add_meme_with_int_in_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "url": 3,
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = do_post.add_meme(data)
        assert response.status_code == 400

    def test_unauthorized_access(self, unauthorized_do_get, unauthorized_do_post,
                                 unauthorized_do_put, unauthorized_do_delete, anatoliy_memes):

        response = unauthorized_do_get.get_all_memes()
        assert response.status_code == 401

        # GET /meme/<id>
        response = unauthorized_do_get.get_all_memes()
        assert response.status_code == 401

        # POST /meme
        data = {
            "text": "Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        response = unauthorized_do_post.add_meme(data)
        assert response.status_code == 401

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
        assert response.status_code == 401

        # DELETE /meme/<id>
        response = unauthorized_do_delete.delete_meme(meme_to_update["id"])
        assert response.status_code == 401
