
def test_register_raw(api_manager, random_user_payload):
    api_manager.auth_api.registration(random_user_payload)


def test_login_user(api_manager, registered_user):
    api_manager.auth_api.login(registered_user)

def test_logout_user(api_manager, registered_user):
    api_manager.auth_api.login(registered_user)
    api_manager.auth_api.logout()

