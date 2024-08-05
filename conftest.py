import pytest
from endpoints.do_post import DoPost
from endpoints.do_get import DoGet
from endpoints.do_put import DoPut
from endpoints.do_delete import DoDelete
from endpoints.authorization import Authorization


@pytest.fixture(scope="session")
def token():
    do_auth = Authorization()
    response = do_auth.authorize("Anatoliy")
    return response.json()["token"]


@pytest.fixture
def authorization():
    return Authorization()


@pytest.fixture
def do_get(token):
    return DoGet(token)


@pytest.fixture
def do_post(token):
    return DoPost(token)


@pytest.fixture
def do_put(token):
    return DoPut(token)


@pytest.fixture
def do_delete(token):
    return DoDelete(token)


@pytest.fixture
def meme_data():
    return {
        "text": "Zoning Out Black Cat",
        "url": "https://i.kym-cdn.com/entries/icons/original/000/045/575/blackcatzoningout_meme.jpg",
        "tags": ["black", "cat"],
        "info": {"colours": ["black", "red"]}
    }


@pytest.fixture
def meme(do_post, do_delete, meme_data):
    response = do_post.add_meme(meme_data)
    assert response.status_code == 200
    meme = response.json()
    yield meme
    do_delete.delete_meme(meme["id"])


@pytest.fixture
def unauthorized_do_get():
    return DoGet()


@pytest.fixture
def unauthorized_do_post():
    return DoPost()


@pytest.fixture
def unauthorized_do_put():
    return DoPut()


@pytest.fixture
def unauthorized_do_delete():
    return DoDelete()


@pytest.fixture
def authorized_do_get(token):
    return DoGet(token)


@pytest.fixture
def anatoliy_memes(authorized_do_get):
    response = authorized_do_get.get_all_memes()
    assert response.status_code == 200
    memes = response.json().get('data', [])
    return [meme for meme in memes if meme.get('updated_by') == 'Anatoliy']
