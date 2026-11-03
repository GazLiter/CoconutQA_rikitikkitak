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
    manager = ApiManager(session)

    yield manager

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
    body = admin_api_manager.genres_api.create_genre(genre_name).json()
    genre_id = body.get('id')

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
def created_movie(admin_api_manager, created_genre_id, request):
    created_ids = []

    def create(**overrides):
        payload = DataGenerator.movie_payload(created_genre_id)
        payload.update(overrides)

        body = admin_api_manager.movies_api.create_movie(payload).json()
        created_ids.append(body['id'])
        return body

    yield create

    if not request.node.get_closest_marker("no_cleanup"):
        for movie_id in created_ids:
            admin_api_manager.movies_api.delete_movie(movie_id)



@pytest.fixture()
def created_movie_id(created_movie):
    return created_movie()['id']

@pytest.fixture()
def create_3_movies(admin_api_manager, created_genre_id, request):
    movies = []
    movie_ids = []

    for _ in range(3):
        payload = DataGenerator.movie_payload(created_genre_id)

        body = admin_api_manager.movies_api.create_movie(payload).json()
        movies.append(body)
        movie_ids.append(body['id'])

    yield movies

    if not request.node.get_closest_marker("no_cleanup"):
        for movie_id in movie_ids:
            admin_api_manager.movies_api.delete_movie(movie_id)



