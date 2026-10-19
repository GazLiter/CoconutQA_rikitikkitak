import pytest

from constants import INVALID_PARAMS,INVALID_CINEMA,INVALID_TYPE, INVALID_IDS,INVALID_PAYLOAD
from schemas.movies import MOVIE_FIELDS,PAGINATION_FIELDS
from utils.data_generator import DataGenerator


class TestsPositive:

    def test_get_movies_success(self, api_manager):
        body = api_manager.movies_api.get_movies().json()
        movies = body['movies']

        assert isinstance(movies, list), 'Ожидали получить список'
        assert len(movies) > 0, 'Ожидали получить хотя бы один фильм'

        first = movies[0]
        for field, type_of_field in MOVIE_FIELDS.items():
            assert field in first, f'Ожидали поле {field} в {first}'
            assert isinstance(first[field],type_of_field)

        assert isinstance(first['genre']['name'], str )

        for field_pagination, type_pagination in PAGINATION_FIELDS.items():
            assert field_pagination in body, f'Ожидали поле {field_pagination} в {body}'
            assert isinstance(body[field_pagination], type_pagination)



    def test_get_movies_pagesize(self, api_manager):
        pagesize = DataGenerator.random_pagesize()

        response = api_manager.movies_api.get_movies(params={'pageSize': pagesize}).json()

        assert response['pageSize'] == pagesize
        assert len(response['movies']) <= pagesize

    def test_get_movies_page(self,api_manager):
        page1 = DataGenerator.random_page()
        page2 = page1 + 1
        pagesize = DataGenerator.random_pagesize()

        response_1 = api_manager.movies_api.get_movies(params={'page': page1, 'pageSize': pagesize }).json()
        response_2 = api_manager.movies_api.get_movies(params={'page': page2, 'pageSize': pagesize }).json()

        assert response_1['page'] == page1
        assert response_2['page'] == page2
        assert isinstance(response_1['page'], int)
        assert isinstance(response_2['page'], int)

        id_by_page1 =  [movie['id'] for movie in response_1['movies']]
        id_by_page2 = [movie['id'] for movie in response_2['movies']]

        assert id_by_page1, f'Вернулась пустая страница {page1}'
        assert id_by_page2, f'Вернулась пустая страница {page2}'
        assert id_by_page1 != id_by_page2, 'Вернулись одинаковые страницы'

    def test_get_movies_min_price(self,api_manager,created_movie):
        price_movie = created_movie['price']
        body_price = api_manager.movies_api.get_movies(params={'minPrice': price_movie}).json()

        assert body_price['movies'], 'Вернулся пустой список'

        for movie in body_price['movies']:
            assert movie['price'] >= price_movie, 'Цена меньше чем указано в фильтре'

        movie_genre_id = created_movie['genreId']
        body_id_and_price = api_manager.movies_api.get_movies(params={'minPrice': price_movie, 'genreId': movie_genre_id}).json()
        ids_movies = [movie['id'] for movie in body_id_and_price['movies']]

        assert created_movie['id'] in ids_movies, 'Фильма нет в списке'




    @pytest.mark.parametrize("invalid_params", INVALID_PARAMS)
    def test_get_movies_invalid_params(self, api_manager, invalid_params):
        api_manager.movies_api.get_movies(expected_status=400, params=invalid_params)

    @pytest.mark.no_cleanup
    def test_delete_movie(self, admin_api_manager, created_movie_id):
        admin_api_manager.movies_api.delete_movie(created_movie_id)

class TestsNegative:

    def test_create_movie_success_and_delete(self, admin_api_manager, movie_payload):
        response = admin_api_manager.movies_api.post_movie(movie_payload)
        cinema_id = response.json().get('id')
        admin_api_manager.movies_api.delete_movie(cinema_id)

    def test_create_movie_without_admin(self, api_manager, movie_payload):
        api_manager.movies_api.post_movie(movie_payload, expected_status=401)


    @pytest.mark.parametrize("invalid_fields" ,INVALID_CINEMA)
    def test_create_movie_invalid_fields(self, admin_api_manager, movie_payload, invalid_fields):
        movie_copy = movie_payload.copy()
        movie_copy.update(invalid_fields)
        admin_api_manager.movies_api.post_movie(data=movie_copy, expected_status=400)

    def test_create_retry(self, admin_api_manager, movie_payload):
        cinema = admin_api_manager.movies_api.post_movie(movie_payload)
        id_cinema = cinema.json().get('id')
        admin_api_manager.movies_api.post_movie(movie_payload, expected_status=409)
        admin_api_manager.movies_api.delete_movie(id_cinema)

    def test_get_movie_by_id(self, api_manager, created_movie_id):
        api_manager.movies_api.get_movie_by_id(created_movie_id)

    def test_get_movie_by_invalid_id(self, api_manager, created_movie_id, admin_api_manager):
        admin_api_manager.movies_api.delete_movie(created_movie_id)
        api_manager.movies_api.get_movie_by_id(created_movie_id, expected_status=404)


    @pytest.mark.xfail(reason="Баг: отдает 500 вместо 404 на неверный тип данных (по Swagger)")
    @pytest.mark.parametrize('invalid_types , expected_code', INVALID_TYPE)
    def test_get_movie_by_invalid_id_types(self, api_manager, invalid_types, expected_code):
        api_manager.movies_api.get_movie_by_id(invalid_types, expected_status=expected_code)




    @pytest.mark.xfail(reason="Возвращает 404 вместо 400 по Swagger на неверный тип данных")
    @pytest.mark.parametrize('invalid_types', ["name",True,24.5])
    def test_delete_movie_invalid_types(self, admin_api_manager, invalid_types):
        admin_api_manager.movies_api.delete_movie(invalid_types, expected_status=400)


    def test_delete_movie_not_found(self, admin_api_manager, created_movie_id):
        admin_api_manager.movies_api.delete_movie(created_movie_id)
        admin_api_manager.movies_api.delete_movie(created_movie_id, expected_status=404)


    def test_update_movie_success(self, admin_api_manager, created_movie_id, movie_payload):
        admin_api_manager.movies_api.patch_movie_by_id(id_movie=created_movie_id, data=movie_payload)


    @pytest.mark.xfail(reason="Баг: 404 вместо 400 на неверный тип ID")
    @pytest.mark.parametrize('invalid', INVALID_IDS)
    def test_update_movie_invalid_id(self, admin_api_manager, invalid, movie_payload):
        admin_api_manager.movies_api.patch_movie_by_id(movie_payload, invalid, expected_status=400)


    @pytest.mark.parametrize('invalid_fields_patch', INVALID_PAYLOAD, ids=[str(item) for item in INVALID_PAYLOAD])
    def test_update_movie_invalid_types_payload(self, admin_api_manager, created_movie_id, invalid_fields_patch,
                                                movie_payload):
        copy_payload = movie_payload.copy()
        copy_payload.update(invalid_fields_patch)
        admin_api_manager.movies_api.patch_movie_by_id(data=copy_payload, id_movie=created_movie_id, expected_status=400)


    def test_update_no_cinema(self, admin_api_manager, created_movie_id, movie_payload):
        admin_api_manager.movies_api.delete_movie(created_movie_id)
        admin_api_manager.movies_api.patch_movie_by_id(id_movie=created_movie_id, data=movie_payload, expected_status=404)



def get_movies_pagination(api_manager, created_movie):
    movie_pagesize = created_movie['pageSize']
    request = api_manager.movies_api.get_movies(params={'pageSize': movie_pagesize}).json
    print(request)
