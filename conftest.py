
import pytest
import requests


from clients.api_manager import ApiManager
from config.admin_credentials import ADMIN_CREDENTIALS
from utils.data_generator import DataGenerator


# ==========================================
# 1. МЕНЕДЖЕРЫ
# ==========================================


@pytest.fixture()
def api_manager():
    session = requests.Session()
    request = ApiManager(session)

    yield request

    session.close()


@pytest.fixture()
def admin_api_manager(admin_credentials):
    session = requests.Session()
    manager = ApiManager(session)

    response = manager.auth_api.login(admin_credentials)
    token = response.json().get('accessToken')
    manager.session.headers.update({'Authorization': f'Bearer {token}'})

    yield manager

    session.close()


@pytest.fixture()
def admin_credentials():
    return ADMIN_CREDENTIALS


# ==========================================
# 2. ПОЛЬЗОВАТЕЛИ
# ==========================================


@pytest.fixture()
def registered_user(api_manager):
    data = DataGenerator.user_payload()
    api_manager.auth_api.registration(data)
    return {'email': data['email'], 'password': data['password']}

@pytest.fixture()
def random_user_payload():
    return DataGenerator.user_payload()


# ==========================================
# 3. ЖАНРЫ
# ==========================================


@pytest.fixture()
def genre_name():
    return DataGenerator.name_movie()

@pytest.fixture()
def created_genre_id(admin_api_manager, genre_name, request):
    response = admin_api_manager.genres_api.create_genre(genre_name)
    genre_id = response.json().get('id')

    yield genre_id

    if not request.node.get_closest_marker("no_cleanup"):
        admin_api_manager.genres_api.delete_genre(genre_id)




# ==========================================
# 4. ФИЛЬМЫ
# ==========================================


@pytest.fixture()
def movie_payload(created_genre_id):
    return DataGenerator.movie_payload(created_genre_id)


@pytest.fixture()
def created_movie(admin_api_manager, movie_payload, request):
    movie = admin_api_manager.movies_api.post_movie(movie_payload).json()

    yield movie

    if not request.node.get_closest_marker("no_cleanup"):
        admin_api_manager.movies_api.delete_movie(movie['id'])


@pytest.fixture()
def created_movie_id(created_movie):
    return created_movie['id']






