import pytest


class TestMemeAPI:

    @pytest.mark.smoke
    def test_authorization(self, authorization):
        authorization.authorize("Anatoliy")
        authorization.check_status_code(200)

    @pytest.mark.regression
    def test_valid_token(self, do_get, token):
        do_get.check_token(token)
        do_get.check_status_code(200)

    @pytest.mark.regression
    def test_get_all_memes(self, do_get):
        do_get.get_all_memes()
        do_get.check_status_code(200)

    @pytest.mark.regression
    def test_get_meme_by_id(self, meme, do_get, meme_data):
        meme_id = meme["id"]
        do_get.get_meme_by_id(meme_id)
        do_get.check_status_code(200)
        do_get.check_meme_data(meme_data)

    @pytest.mark.smoke
    def test_add_meme(self, do_post, meme_data):
        do_post.add_meme(meme_data)
        do_post.check_status_code(200)
        do_post.check_meme_data(meme_data)

    @pytest.mark.extended
    def test_update_meme(self, meme, do_put, do_get):
        meme_id = meme["id"]
        updated_data = {
            "id": meme_id,
            "text": "I like the meme named Zoning Out Black Cat",
            "url": meme["url"],
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        do_put.update_meme(meme_id, updated_data)
        do_put.check_status_code(200)

        do_get.get_meme_by_id(meme_id)
        do_get.check_status_code(200)
        do_get.check_meme_data(updated_data)

    @pytest.mark.smoke
    def test_delete_meme(self, meme, do_delete, do_get):
        meme_id = meme["id"]

        do_delete.delete_meme(meme_id)
        do_delete.check_status_code(200)

        do_get.get_meme_by_id(meme_id)
        do_get.check_status_code(404)

    @pytest.mark.extended
    def test_invalid_token(self, do_get):
        do_get.check_token("xsdsd232333")
        do_get.check_status_code(404)

    @pytest.mark.extended
    def test_nonexistent_meme(self, do_get):
        do_get.get_meme_by_id("3234348949493x")
        do_get.check_status_code(404)

    @pytest.mark.extended
    def test_add_meme_without_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        do_post.add_meme(data)
        do_post.check_status_code(400)

    @pytest.mark.extended
    def test_update_meme_with_nonexistent_id(self, do_put):
        data = {
            "id": "3234348949493x",
            "text": "I like the meme named Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat", "green eyes"],
            "info": {"colours": ["black", "red", "green"]}
        }
        do_put.update_meme("3234348949493x", data)
        do_put.check_status_code(404)

    @pytest.mark.extended
    def test_delete_meme_created_by_other_user(self, do_delete, other_user_meme):
        meme_id = other_user_meme["id"]
        do_delete.delete_meme(meme_id)
        do_delete.check_status_code(403)

    @pytest.mark.extended
    def test_add_meme_with_int_in_text(self, do_post):
        data = {
            "text": 3,
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        do_post.add_meme(data)
        do_post.check_status_code(400)

    @pytest.mark.extended
    def test_add_meme_with_int_in_url(self, do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "url": 3,
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        do_post.add_meme(data)
        do_post.check_status_code(400)

    @pytest.mark.extended
    def test_unauthorized_access_get(self, unauthorized_do_get):
        unauthorized_do_get.get_all_memes()
        unauthorized_do_get.check_status_code(401)

    @pytest.mark.extended
    def test_unauthorized_access_post(self, unauthorized_do_post):
        data = {
            "text": "Zoning Out Black Cat",
            "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
            "tags": ["black", "cat"],
            "info": {"colours": ["black", "red"]}
        }
        unauthorized_do_post.add_meme(data)
        unauthorized_do_post.check_status_code(401)

    @pytest.mark.extended
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
        unauthorized_do_put.update_meme(meme_to_update["id"], updated_data)
        unauthorized_do_put.check_status_code(401)

    @pytest.mark.extended
    def test_unauthorized_access_delete(self, unauthorized_do_delete, anatoliy_memes):
        meme_to_delete = next((m for m in anatoliy_memes), None)
        assert meme_to_delete is not None, "No meme found created by Anatoliy"

        unauthorized_do_delete.delete_meme(meme_to_delete["id"])
        unauthorized_do_delete.check_status_code(401)
