import pytest
from constants import INVALID_PARAMS,INVALID_CINEMA,INVALID_TYPE, INVALID_IDS,INVALID_PAYLOAD


def test_get_movies(manager_with_session):
    manager_with_session.movies_api.get_movies()

def test_get_movies_with_params(manager_with_session):
    manager_with_session.movies_api.get_movies(params={'pageSize': 5, 'page': 2,'locations': 'SPB'})

@pytest.mark.parametrize("invalid_params", INVALID_PARAMS)
def test_get_movies_invalid_params(manager_with_session,invalid_params ):
    manager_with_session.movies_api.get_movies(expected_status=400,params=invalid_params)



def test_create_movie(manager_super,cinema_payload):
    response = manager_super.movies_api.post_movies(cinema_payload)
    cinema_id = response.json().get('id')
    manager_super.movies_api.delete_movies(cinema_id)

def test_create_movie_without_admin(manager_with_session,cinema_payload):
    manager_with_session.movies_api.post_movies(cinema_payload,expected_status=401)


@pytest.mark.parametrize("invalid_fields" ,INVALID_CINEMA)
def test_create_movie_invalid_fields(manager_super,cinema_payload,invalid_fields):
    movie_copy = cinema_payload.copy()
    movie_copy.update(invalid_fields)
    manager_super.movies_api.post_movies(data=movie_copy,expected_status=400)

def test_create_retry(manager_super,cinema_payload):
    cinema = manager_super.movies_api.post_movies(cinema_payload)
    id_cinema = cinema.json().get('id')
    manager_super.movies_api.post_movies(cinema_payload,expected_status=409)
    manager_super.movies_api.delete_movies(id_cinema)

def test_get_movie_on_id(manager_with_session,take_id_of_cinema_with_delete):
    manager_with_session.movies_api.get_cinema_on_id(take_id_of_cinema_with_delete)

def test_get_movie_on_invalid_id(manager_with_session,take_id_of_cinema,manager_super):
    manager_super.movies_api.delete_movies(take_id_of_cinema)
    manager_with_session.movies_api.get_cinema_on_id(take_id_of_cinema, expected_status=404)

#Тест на подстановку разных типов данных на место ID
@pytest.mark.xfail(reason="Баг: отдает 500 вместо 404 на неверный тип данных (по Swagger)")
@pytest.mark.parametrize('invalid_types , expected_code', INVALID_TYPE)
def test_get_movie_on_invalid_id_types(manager_with_session,invalid_types,expected_code):
    manager_with_session.movies_api.get_cinema_on_id(invalid_types, expected_status=expected_code)

def test_delete_cinema(manager_super, take_id_of_cinema):
    manager_super.movies_api.delete_movies(take_id_of_cinema)

#Тест на подстановку разных типов данных на место ID
@pytest.mark.xfail(reason="Возвращает 404 вместо 400 по Swagger на неверный тип данных")
@pytest.mark.parametrize('invalid_types', ["name",True,24.5])
def test_delete_cinema_invalid_types(manager_super,invalid_types):
    manager_super.movies_api.delete_movies(invalid_types,expected_status=400)

#Удаление несуществующего теста
def test_delete_404(manager_super,take_id_of_cinema):
    manager_super.movies_api.delete_movies(take_id_of_cinema)
    manager_super.movies_api.delete_movies(take_id_of_cinema, expected_status=404)

#Позитивный тест на PATCH
def test_patch_cinema(manager_super,take_id_of_cinema_with_delete,cinema_payload):
    manager_super.movies_api.patch_cinema_on_id(id_cinema=take_id_of_cinema_with_delete,data=cinema_payload)

#Тест на разные типы данных в ID PATCH
@pytest.mark.xfail(reason="Баг: 404 вместо 400 на неверный тип ID")
@pytest.mark.parametrize('invalid', INVALID_IDS)
def test_patch_cinema_invalid_id(manager_super, invalid, cinema_payload):
    manager_super.movies_api.patch_cinema_on_id(cinema_payload,invalid, expected_status=400)

#Тест на разные типы данных в поля при PATCH
@pytest.mark.parametrize('invalid_fields_patch', INVALID_PAYLOAD, ids=[str(item) for item in INVALID_PAYLOAD])
def test_patch_cinema_invalid_types_payload(manager_super,take_id_of_cinema_with_delete , invalid_fields_patch, cinema_payload):
    copy_payload = cinema_payload.copy()
    copy_payload.update(invalid_fields_patch)
    manager_super.movies_api.patch_cinema_on_id(data=copy_payload, id_cinema=take_id_of_cinema_with_delete, expected_status=400)

#Тест PATCH на несуществующий фильм
def test_patch_no_cinema(manager_super,take_id_of_cinema,cinema_payload):
    manager_super.movies_api.delete_movies(take_id_of_cinema)
    manager_super.movies_api.patch_cinema_on_id(id_cinema=take_id_of_cinema,data=cinema_payload, expected_status=404)
