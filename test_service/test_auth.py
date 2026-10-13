
def test_register_raw(manager_with_session, data_full):
    manager_with_session.auth_api.registration(data_full)


def test_login_user(manager_with_session, registration_and_data_for_login):
    manager_with_session.auth_api.login(registration_and_data_for_login)

def test_logout_user(manager_with_session,registration_and_data_for_login):
    manager_with_session.auth_api.login(registration_and_data_for_login)
    manager_with_session.auth_api.logout()

