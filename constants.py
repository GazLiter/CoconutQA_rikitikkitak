import pytest

INVALID_PARAMS = [
    {"locations": "NY"},
    {"page": -1},
    {"createdAt": "random"},
    {"genreId": "text"},
    {"minPrice": -100}
]

INVALID_CINEMA = [
    {"name": 1},
    {"imageUrl": 1},
    {"price": "100"},
    {"description": 222},
    {"location": "NY"},
    {"published": 1},
    {"genreId": 'huinya'}
]

INVALID_TYPE = [
    ("name", 500),
    (True, 500),
    (24.5, 404)
]

INVALID_IDS = [
    "name",
    True,
    24.5
]




RAW_PAYLOADS = [
    # 1. name (строка)
    {"name": 123}, {"name": None}, {"name": []}, {"name": True}, {'name': {}},

    # 2. description (строка)
    {"description": 123}, {"description": None}, {"description": []}, {"description": False},

    # 3. price (число)
    {"price": "error"}, {"price": None}, {"price": []}, {"price": True},

    # 4. location (строка, только MSK или SPB)
    {"location": "UFA"}, {"location": 123}, {"location": None}, {"location": []},

    # 5. imageUrl (строка)
    {"imageUrl": 123}, {"imageUrl": None}, {"imageUrl": []}, {"imageUrl": False},

    # 6. published (булево значение)
    {"published": "true"}, {"published": 123}, {"published": None}, {"published": []},

    # 7. genreId (число)
    {"genreId": "id"}, {"genreId": None}, {"genreId": []}, {"genreId": False},


]

INVALID_PAYLOAD = []

for item in RAW_PAYLOADS:
    key, value = list(item.items())[0]

    if value is None:
        bug_reason = "Баг 200" if key == "imageUrl" else "Баг 404"
        # Добавляем маркер и красивое имя (id)
        INVALID_PAYLOAD.append(pytest.param(item, marks=pytest.mark.xfail(reason=bug_reason), id=str(item)))
    else:
        # Оборачиваем обычные проверки в pytest.param только ради красивого имени
        INVALID_PAYLOAD.append(pytest.param(item, id=str(item)))




