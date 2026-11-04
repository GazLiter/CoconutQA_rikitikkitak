
import pytest
from faker import Faker

fake = Faker()

INVALID_PARAMS = [

    pytest.param({"locations": fake.word()}, id="locations_string"),
    pytest.param({"locations": fake.random_int()}, id="locations_int"),
    pytest.param({"locations": fake.boolean()}, id="locations_bool"),
    pytest.param({"locations": ""}, id="locations_empty"),
    pytest.param({"locations": " "}, id="locations_space"),

    pytest.param({"page": fake.random_int(min=-1000, max=-1)}, id="page_negative"),
    pytest.param({"page": 0}, id="page_zero"),
    pytest.param({"page": fake.boolean()}, id="page_bool"),
    pytest.param({"page": ""}, id="page_empty"),
    pytest.param({"page": " "}, id="page_space"),

    pytest.param({"pageSize": fake.random_int(min=-1000, max=0)}, id="pageSize_invalid_int"),
    pytest.param({"pageSize": fake.word()}, id="pageSize_string"),
    pytest.param({"pageSize": fake.boolean()}, id="pageSize_bool"),
    pytest.param({"pageSize": ""}, id="pageSize_empty"),
    pytest.param({"pageSize": " "}, id="pageSize_space"),

    pytest.param({"createdAt": fake.word()}, id="createdAt_invalid_string"),

    pytest.param({"genreId": fake.word()}, id="genreId_string"),
    pytest.param({"genreId": fake.boolean()}, id="genreId_bool"),
    pytest.param({"genreId": fake.random_int(min=-1000, max=-1)}, id="genreId_negative"),
    pytest.param({"genreId": ""}, id="genreId_empty"),
    pytest.param({"genreId": " "}, id="genreId_space"),

    pytest.param({"minPrice": fake.random_int(min=-1000, max=-1)}, id="minPrice_negative"),
    pytest.param({"minPrice": fake.word()}, id="minPrice_string"),
    pytest.param({"minPrice": fake.boolean()}, id="minPrice_bool"),

    pytest.param({"maxPrice": fake.random_int(min=-1000, max=-1)}, id="maxPrice_negative"),
    pytest.param({"maxPrice": fake.word()}, id="maxPrice_string"),
    pytest.param({"maxPrice": fake.boolean()}, id="maxPrice_bool"),

    pytest.param({"minPrice": 1000, "maxPrice": 1}, id="minPrice_greater_than_maxPrice"),
]

INVALID_PAYLOADS = [

    pytest.param({"name": ""}, id="name_empty"),
    pytest.param({"name": " "}, id="name_space"),
    pytest.param({"name": fake.random_int()}, id="name_int"),

    pytest.param({"price": fake.random_int(min=-1000, max=-1)}, id="price_negative"),
    pytest.param({"price": fake.word()}, id="price_string"),
    pytest.param({"price": fake.boolean()}, id="price_bool"),

    pytest.param({"location": fake.word()}, id="location_invalid_enum"),
    pytest.param({"location": fake.random_int()}, id="location_int"),

    pytest.param({"published": fake.word()}, id="published_string"),
    pytest.param({"published": fake.random_int()}, id="published_int"),

    pytest.param({"genreId": fake.word()}, id="genreId_string"),
    pytest.param({"genreId": fake.random_int(min=-1000, max=-1)}, id="genreId_negative"),
    pytest.param({"genreId": fake.boolean()}, id="genreId_bool"),
]


INVALID_TYPE_MOVIE_ID = [
    (fake.pystr(), 500),
    (fake.boolean(), 500),
    (fake.pyfloat(), 404),
    (" ", 404),
    (fake.random_int(min=-1000, max=-1), 404),
    (0, 404),
    (99999999999999999999999999999999, 500)
]


INVALID_TYPE_DELETE_MOVIE_ID = [
    (fake.pystr()),
    (fake.boolean()),
    (fake.pyfloat()),
    (" "),
    (fake.random_int(min=-1000, max=-1)),
    (0),
    (99999999999999999999999999999999)
]

INVALID_TYPE_UPDATE_MOVIE_ID = [
    (fake.pystr()),
    (fake.boolean()),
    (fake.pyfloat()),
    (" "),
    (fake.random_int(min=-1000, max=-1)),
    (0),
    (99999999999999999999999999999999)
]




INVALID_TYPE_UPDATE_MOVIE_PAYLOAD = [

    {"name": fake.random_int()},
    {"name": fake.boolean()},
    {'name': fake.pyfloat()},
    {"name": fake.random_int(min=-1000, max=-1)},
    {"name": None},
    {"name": []},
    {'name': {}},
    {'name': ""},
    {'name': " "},
    {'name': 0},


    {"description": fake.random_int()},
    {"description": fake.random_int(min=-1000, max=-1)},
    {"description": fake.boolean()},
    {"description": fake.pyfloat()},
    {"description": None},
    {"description": []},
    {"description": {}},
    {"description": ""},
    {"description": " "},
    {"description": 0},


    {"price": fake.pystr()},
    {"price": fake.boolean()},
    {"price": fake.pyfloat()},
    {"price": None},
    {"price": []},
    {"price": {}},
    {"price": ""},
    {"price": " "},
    {"price": 0},
    {"price": fake.random_int(min=-1000, max=-1)},


    {"location": fake.city()},
    {"location": fake.random_int()},
    {"location": fake.boolean()},
    {"location": None},
    {"location": []},


    {"imageUrl": fake.random_int()},
    {"imageUrl": fake.boolean()},
    {"imageUrl": fake.pystr()},
    {"imageUrl": None},
    {"imageUrl": []},
    {"imageUrl": ""},


    {"published": fake.pystr()},
    {"published": fake.random_int()},
    {"published": None},
    {"published": []},


    {"genreId": fake.pystr()},
    {"genreId": fake.boolean()},
    {"genreId": fake.pyfloat()},
    {"genreId": fake.random_int(min=-1000, max=0)},
    {"genreId": None},
    {"genreId": []},
]


