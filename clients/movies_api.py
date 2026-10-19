from diy_requester.diy_requester import DiyRequester
from config.base_urls import MOVIES_URL


class MoviesApi(DiyRequester):
    def __init__(self,session):
        super().__init__(session= session, central_url=MOVIES_URL)

    def get_movies(self,expected_status=200, params=None,**kwargs):
        return self.send_request(
            method='GET',
            expected_status=expected_status,
            params=params,
            **kwargs

        )

    def post_movie(self, data, expected_status=201):
        return self.send_request(
            method='POST',
            expected_status=expected_status,
            json=data
        )

    def delete_movie(self, id_movie:int, expected_status=200):
        return self.send_request(
            method='DELETE',
            endpoint=f'/{id_movie}',
            expected_status=expected_status
        )

    def get_movie_by_id(self, id_movie:int, expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=f'/{id_movie}',
            expected_status=expected_status
        )

    def patch_movie_by_id(self, id_movie:int, data, expected_status=200):
        return self.send_request(
            method='PATCH',
            endpoint=f'/{id_movie}',
            expected_status=expected_status,
            json=data
        )