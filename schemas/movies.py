MOVIE_FIELDS = {
    'id': int,
    'name': str,
    'description': str,
    'genreId': int,
    'imageUrl': str,
    'price': int,
    'published': bool,
    'rating': int,
    'location': str,
    'createdAt': str,
}

PAGINATION_FIELDS = {
    'count': int,
    'page': int,
    'pageSize': int,
    'pageCount': int,
}
