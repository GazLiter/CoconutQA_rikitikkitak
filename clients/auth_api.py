from config.base_urls import AUTH_URL
from diy_requester.diy_requester import DiyRequester

class AuthApi(DiyRequester):
    REGISTER = '/register'
    LOGIN = '/login'
    LOGOUT = '/logout'

    def __init__(self,session):
        super().__init__(session=session, central_url=AUTH_URL)

    def login(self,data):
        return self.send_request(
            'POST',
            endpoint=self.LOGIN,
            expected_status=200,
            json=data
        )




    def registration(self,data):
        return self.send_request(
            'POST',
            self.REGISTER,
            expected_status=201,
            json=data
        )

    def logout(self):
        return self.send_request(
            method='GET',
            endpoint=self.LOGOUT,
            expected_status=200
        )