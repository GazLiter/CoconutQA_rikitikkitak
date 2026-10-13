from diy_requester.diy_requester import DiyRequester
from config.base_urls import MOVIES_URL


class MoviesApi(DiyRequester):
    def __init__(self,session):
        super().__init__(session= session, central_url=MOVIES_URL)

    def get_movies(self,expected_status=200,params=None,**kwargs):
        return self.send_request(
            method='GET',
            expected_status=expected_status,
            params=params,
            **kwargs

        )

    def post_movies(self,data,expected_status=201):
        return self.send_request(
            method='POST',
            expected_status=expected_status,
            json=data
        )

    def delete_movies(self, id=int, expected_status=200):
        return self.send_request(
            method='DELETE',
            endpoint=f'/{id}',
            expected_status=expected_status
        )

    def get_cinema_on_id(self, id_cinema=int,expected_status=200):
        return self.send_request(
            method='GET',
            endpoint=f'/{id_cinema}',
            expected_status=expected_status
        )

    def patch_cinema_on_id(self,data,id_cinema=int,expected_status=200):
        return self.send_request(
            method='PATCH',
            endpoint=f'/{id_cinema}',
            expected_status=expected_status,
            json=data
        )