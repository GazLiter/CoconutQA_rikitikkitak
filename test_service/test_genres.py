

def test_get_genres(manager_with_session):
    manager_with_session.genres_api.get_genres()

def test_create_genre(manager_super,name_cinema):
    manager_super.genres_api.create_genres(name_cinema)

def test_delete_genres(manager_super, get_genre_id):
    manager_super.genres_api.delete_genres(get_genre_id)

def test_get_cinema_on_id(manager_with_session, get_genre_id_delete):
    manager_with_session.genres_api.get_cinema_on_id(get_genre_id_delete)

