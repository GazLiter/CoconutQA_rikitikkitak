from diy_requester.diy_requester import DiyRequester
from config.base_urls import GENRES_URL

class GenresApi(DiyRequester):
    def __init__(self,session):
        super().__init__(session= session, central_url=GENRES_URL)

    def get_genres(self):
        return self.send_request(
            method='GET',
            expected_status=200,
        )

    def create_genre(self, name):
        return self.send_request(
            method='POST',
            json={'name': name},
            expected_status= 201
        )

    def delete_genre(self, id_genre):
        return self.send_request(
            'DELETE',
            expected_status=200,
            endpoint=f'/{id_genre}'
        )

    def get_movie_by_id(self, id_genre):
        return self.send_request(
            method='GET',
            expected_status=200,
            endpoint=f'/{id_genre}'
        )