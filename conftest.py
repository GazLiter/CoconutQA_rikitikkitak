#Фикстуры
import pytest
import requests


from clients.api_meneger import ApiManager
from utils.data_generator import DataGenerator

@pytest.fixture()
def manager_with_session():
    session = requests.Session()
    request = ApiManager(session)

    yield request

    session.close()


@pytest.fixture()
def manager_super(admin_user):
    session = requests.Session()
    manager = ApiManager(session)

    response = manager.auth_api.login(admin_user)
    token = response.json().get('accessToken')
    manager.session.headers.update({'Authorization': f'Bearer {token}'})

    yield manager

    session.close()


@pytest.fixture()
def admin_user():
    return {'email': 'api1@gmail.com', 'password': 'asdqwe123Q'}

@pytest.fixture()
def registration_and_data_for_login(manager_with_session):
    data = DataGenerator.user_payload()
    manager_with_session.auth_api.registration(data)
    return {'email': data['email'], 'password': data['password']}

@pytest.fixture()
def data_full():
    return DataGenerator.user_payload()

@pytest.fixture()
def name_cinema():
    return DataGenerator.name_cinema()

@pytest.fixture()
def get_genre_id(manager_super, name_cinema):
    response = manager_super.genres_api.create_genres(name_cinema)
    id_cinema = response.json().get('id')
    return id_cinema



@pytest.fixture()
def get_genre_id_delete(manager_super, name_cinema):
    response = manager_super.genres_api.create_genres(name_cinema)
    id_cinema = response.json().get('id')
    yield id_cinema

    manager_super.genres_api.delete_genres(id_cinema)

@pytest.fixture()
def create_cinema_with_delete(manager_super, get_genre_id_delete):
    data = DataGenerator.cinema_payload(get_genre_id_delete)
    cinema = manager_super.movies_api.post_movies(data)

    yield cinema

    cinema_id = cinema.json().get('id')
    manager_super.movies_api.delete_movies(cinema_id)

@pytest.fixture()
def cinema_payload(get_genre_id):
    data = DataGenerator.cinema_payload(get_genre_id)
    return data

@pytest.fixture()
def take_id_of_cinema_with_delete(manager_super,get_genre_id):
    data = DataGenerator.cinema_payload(get_genre_id)
    cinema = manager_super.movies_api.post_movies(data)
    cinema_id = cinema.json().get('id')

    yield cinema_id

    manager_super.movies_api.delete_movies(cinema_id)

@pytest.fixture()
def take_id_of_cinema(manager_super,get_genre_id):
    data = DataGenerator.cinema_payload(get_genre_id)
    cinema = manager_super.movies_api.post_movies(data)
    cinema_id = cinema.json().get('id')

    return cinema_id




