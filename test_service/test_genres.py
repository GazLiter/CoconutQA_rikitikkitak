

def test_get_genres(api_manager):
    api_manager.genres_api.get_genres()

def test_create_genre(admin_api_manager, genre_name):
    admin_api_manager.genres_api.create_genre(genre_name)

def test_delete_genres(admin_api_manager, created_genre_id):
    admin_api_manager.genres_api.delete_genre(created_genre_id)

def test_get_cinema_on_id(api_manager, created_genre_id):
    api_manager.genres_api.get_movie_by_id(created_genre_id)

