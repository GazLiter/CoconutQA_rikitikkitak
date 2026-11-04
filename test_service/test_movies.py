import pytest

from conftest import movie_payload
from schemas.movies import MOVIE_FIELDS, PAGINATION_FIELDS
from utils.data_generator import DataGenerator
from data.payloads.movies import INVALID_PARAMS, INVALID_PAYLOADS, INVALID_TYPE_MOVIE_ID, INVALID_TYPE_DELETE_MOVIE_ID, \
    INVALID_TYPE_UPDATE_MOVIE_ID, INVALID_TYPE_UPDATE_MOVIE_PAYLOAD


def get_invalid_payload(base_payload, invalid_data):
    payload = base_payload.copy()
    payload.update(invalid_data)
    return payload


class TestsPositive:

    def test_get_movies_success(self, api_manager, created_movie):
        created_movie()
        body = api_manager.movies_api.get_movies().json()
        movies = body['movies']

        assert isinstance(movies, list), 'Ожидали получить список'
        assert len(movies) > 0, 'Ожидали получить хотя бы один фильм'

        first_movie = movies[0]
        for field, type_of_field in MOVIE_FIELDS.items():
            assert field in first_movie, f'Ожидали поле {field} в {first_movie}'
            assert isinstance(first_movie[field], type_of_field), f"Поле {field} ожидали {type_of_field}, получили {type(first_movie[field])}"

        assert isinstance(first_movie['genre']['name'], str)

        for field_pagination, type_pagination in PAGINATION_FIELDS.items():
            assert field_pagination in body, f'Ожидали поле {field_pagination} в {body}'
            assert isinstance(body[field_pagination], type_pagination)

    def test_get_movies_pagesize_success(self, api_manager):
        pagesize = DataGenerator.random_pagesize()

        body = api_manager.movies_api.get_movies(params={'pageSize': pagesize}).json()

        assert body['pageSize'] == pagesize
        assert len(body['movies']) <= pagesize

    def test_get_movies_page_success(self, api_manager):
        page1 = DataGenerator.random_page()
        page2 = page1 + 1
        pagesize = DataGenerator.random_pagesize()

        response_1 = api_manager.movies_api.get_movies(params={'page': page1, 'pageSize': pagesize}).json()
        response_2 = api_manager.movies_api.get_movies(params={'page': page2, 'pageSize': pagesize}).json()

        assert response_1['page'] == page1
        assert response_2['page'] == page2
        assert isinstance(response_1['page'], int)
        assert isinstance(response_2['page'], int)

        id_by_page1 = [movie['id'] for movie in response_1['movies']]
        id_by_page2 = [movie['id'] for movie in response_2['movies']]

        assert id_by_page1, f'Вернулась пустая страница {page1}'
        assert id_by_page2, f'Вернулась пустая страница {page2}'
        assert id_by_page1 != id_by_page2, 'Вернулись одинаковые страницы'

    def test_get_movies_min_price_success(self, api_manager, created_movie):
        movie_price = created_movie()['price']
        body = api_manager.movies_api.get_movies(params={'minPrice': movie_price}).json()

        assert body['movies'], 'Вернулся пустой список'

        for movie in body['movies']:
            assert movie['price'] >= movie_price, 'Цена меньше чем указано в фильтре'
            assert isinstance(movie['price'], int)

    def test_get_movies_max_price_success(self, api_manager, created_movie):
        movie_price = created_movie()['price']
        body = api_manager.movies_api.get_movies(params={'maxPrice': movie_price}).json()

        assert body['movies'], 'Вернулся пустой список'

        for movie in body['movies']:
            assert movie['price'] <= movie_price, 'Цена больше чем указано в фильтре'
            assert isinstance(movie['price'], int)

    def test_get_movies_location_spb_success(self, api_manager, created_movie):
        created_movie(location='SPB')
        body = api_manager.movies_api.get_movies(params={'locations': ['SPB']}).json()

        assert body['movies'], 'Вернулся пустой список'

        for movie in body['movies']:
            assert movie['location'] == 'SPB'
            assert isinstance(movie['location'], str)

    def test_get_movies_location_msk_success(self, api_manager, created_movie):
        created_movie(location='MSK')
        body = api_manager.movies_api.get_movies(params={'locations': ['MSK']}).json()

        assert body['movies'], 'Вернулся пустой список'

        for movie in body['movies']:
            assert movie['location'] == 'MSK'
            assert isinstance(movie['location'], str)

    def test_get_movies_published_true_success(self, api_manager, created_movie):
        created_movie()
        body = api_manager.movies_api.get_movies(params={'published': 'true'}).json()

        assert body['movies'], 'Вернулся пустой список'

        for movie in body['movies']:
            assert movie['published'] is True
            assert isinstance(movie['published'], bool)

    def test_get_movies_published_false_success(self, api_manager, created_movie):
        created_movie(published=False)
        body = api_manager.movies_api.get_movies(params={'published': 'false'}).json()

        assert body['movies'], 'Вернулся пустой список'

        for movie in body['movies']:
            assert movie['published'] is False
            assert isinstance(movie['published'], bool)

    def test_get_movies_genre_id_success(self, api_manager, created_movie):
        movie_genre_id = created_movie()['genreId']
        body = api_manager.movies_api.get_movies(params={'genreId': movie_genre_id}).json()

        assert body['movies'], 'Вернулся пустой список'

        for movie in body['movies']:
            assert movie['genreId'] == movie_genre_id

    def test_get_movies_created_at_asc_success(self, api_manager, created_movie):
        created_movie()
        created_movie()
        created_movie()
        body = api_manager.movies_api.get_movies(params={'createdAt': 'asc'}).json()

        assert body['movies'], 'Вернулся пустой список'

        dates = [movie['createdAt'] for movie in body['movies']]

        assert dates == sorted(dates), f'Не отсортировано по asc: {dates}'

    def test_get_movies_created_at_desc_success(self, api_manager, created_movie):
        created_movie()
        created_movie()
        created_movie()
        body = api_manager.movies_api.get_movies(params={'createdAt': 'desc'}).json()

        assert body['movies'], 'Вернулся пустой список'

        dates = [movie['createdAt'] for movie in body['movies']]

        assert dates == sorted(dates, reverse=True), f'Не отсортировано по desc: {dates}'

    def test_get_movie_by_id_success(self, api_manager, created_movie_id):
        body = api_manager.movies_api.get_movie_by_id(created_movie_id).json()

        assert body, 'Вернулся пустой ответ'
        assert body['id'] == created_movie_id

        for field, type_of_field in MOVIE_FIELDS.items():
            assert field in body, f'Ожидали поле {field} в ответе'
            assert isinstance(body[field], type_of_field), f'Поле {field} должно быть {type_of_field}'

    def test_create_movie_success(self, admin_api_manager, movie_payload):
        body = admin_api_manager.movies_api.create_movie(data=movie_payload).json()

        assert body, 'Вернулся пустой ответ'

        for field, type_of_field in MOVIE_FIELDS.items():
            assert field in body, f'Ожидали получить поле {field}'
            assert isinstance(body[field], type_of_field)

        for key, value in movie_payload.items():
            assert body[key] == value

        admin_api_manager.movies_api.delete_movie(body['id'])

    def test_update_movie_success(self, admin_api_manager, created_movie_id, movie_payload):
        body_update = admin_api_manager.movies_api.update_movie(created_movie_id, data=movie_payload).json()

        assert body_update, 'Вернулся пустой ответ'

        for field, type_of_field in MOVIE_FIELDS.items():
            assert field in body_update, f'Ожидали поле {field} в ответе'
            assert isinstance(body_update[field], type_of_field), f'Поле {field} должно быть {type_of_field}'

        body_get = admin_api_manager.movies_api.get_movie_by_id(created_movie_id).json()

        for key, value in movie_payload.items():
            assert key in body_get, f"Поле {key} отсутствует после обновления"
            assert body_get[key] == value, f'Ошибка в поле {key}, ожидали получить {value}, а получили {body_get[key]}'

    @pytest.mark.no_cleanup
    def test_delete_movie_success(self, admin_api_manager, created_movie_id):
        admin_api_manager.movies_api.delete_movie(created_movie_id)
        admin_api_manager.movies_api.get_movie_by_id(created_movie_id, expected_status=404)




class TestsNegative:

    @pytest.mark.parametrize("invalid_params", INVALID_PARAMS)
    def test_get_movies_invalid_params(self, api_manager, invalid_params):
        api_manager.movies_api.get_movies(expected_status=400, params=invalid_params)

    @pytest.mark.parametrize("invalid_data", INVALID_PAYLOADS)
    def test_create_movie_invalid_params(self, admin_api_manager, movie_payload, invalid_data):
        payload = get_invalid_payload(movie_payload, invalid_data)

        admin_api_manager.movies_api.create_movie(data=payload, expected_status=400)

    def test_create_movie_conflict(self, created_movie, admin_api_manager, movie_payload):
        duplicate_name = created_movie()['name']
        payload = movie_payload.copy()
        payload['name'] = duplicate_name

        admin_api_manager.movies_api.create_movie(data=payload, expected_status=409)

    def test_create_movie_unauthorized(self, api_manager, movie_payload):
        api_manager.movies_api.create_movie(movie_payload, expected_status=401)

    def test_create_movie_forbidden(self, api_manager, registered_user, movie_payload):
        response = api_manager.auth_api.login(registered_user).json()
        token = response.get('accessToken')
        api_manager.session.headers.update({'Authorization': f'Bearer {token}'})

        api_manager.movies_api.create_movie(data=movie_payload, expected_status=403)

    def test_get_movie_not_found(self, api_manager):
        api_manager.movies_api.get_movie_by_id(DataGenerator.random_big_int(), expected_status=404)

    @pytest.mark.parametrize('invalid_type, expected_code', INVALID_TYPE_MOVIE_ID)
    def test_get_movie_invalid_id_type(self, api_manager, invalid_type, expected_code):
        api_manager.movies_api.get_movie_by_id(invalid_type, expected_status=expected_code)

    @pytest.mark.bug
    @pytest.mark.parametrize('invalid_type', INVALID_TYPE_DELETE_MOVIE_ID)
    def test_delete_movie_invalid_types(self, admin_api_manager, invalid_type):
        admin_api_manager.movies_api.delete_movie(invalid_type, expected_status=404)

    def test_delete_movie_unauthorized(self, api_manager, created_movie_id):
        api_manager.movies_api.delete_movie(created_movie_id, expected_status=401)

    def test_delete_movie_forbidden(self, api_manager, registered_user, created_movie_id):
        response = api_manager.auth_api.login(registered_user).json()
        token = response.get('accessToken')
        api_manager.session.headers.update({'Authorization': f'Bearer {token}'})

        api_manager.movies_api.delete_movie(created_movie_id, expected_status=403)

    @pytest.mark.no_cleanup
    def test_delete_movie_not_found(self, admin_api_manager, created_movie_id):
        admin_api_manager.movies_api.delete_movie(created_movie_id)
        admin_api_manager.movies_api.delete_movie(created_movie_id, expected_status=404)

    def test_update_movie_unauthorized(self, api_manager, created_movie_id, movie_payload):
        api_manager.movies_api.update_movie(created_movie_id, data=movie_payload, expected_status=401)

    def test_update_movie_forbidden(self, api_manager, registered_user, created_movie_id, movie_payload):
        response = api_manager.auth_api.login(registered_user).json()
        token = response.get('accessToken')
        api_manager.session.headers.update({'Authorization': f'Bearer {token}'})

        api_manager.movies_api.update_movie(created_movie_id, data=movie_payload, expected_status=403)

    @pytest.mark.parametrize('invalid_types', INVALID_TYPE_UPDATE_MOVIE_ID)
    def test_update_movie_invalid_id(self, admin_api_manager, invalid_types, movie_payload):
        admin_api_manager.movies_api.update_movie(movie_id=invalid_types, data=movie_payload, expected_status=404)

    @pytest.mark.no_cleanup
    def test_update_movie_not_found(self, admin_api_manager, created_movie_id, movie_payload):
        admin_api_manager.movies_api.delete_movie(created_movie_id)
        admin_api_manager.movies_api.update_movie(movie_id=created_movie_id, data=movie_payload, expected_status=404)

    @pytest.mark.bugs
    @pytest.mark.parametrize('invalid_fields_patch', INVALID_TYPE_UPDATE_MOVIE_PAYLOAD, ids=[str(item) for item in INVALID_TYPE_UPDATE_MOVIE_PAYLOAD])
    def test_update_movie_invalid_types_payload(self, admin_api_manager, created_movie_id, invalid_fields_patch, movie_payload):
        payload = get_invalid_payload(movie_payload, invalid_fields_patch)
        admin_api_manager.movies_api.update_movie(data=payload, movie_id=created_movie_id, expected_status=400)






