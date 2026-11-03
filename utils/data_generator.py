

from faker import Faker

fake = Faker()

class DataGenerator:

    @staticmethod
    def email():
        return fake.email()

    @staticmethod
    def password():
        return fake.password(length=10)

    @staticmethod
    def name():
        return fake.pystr(min_chars=5, max_chars=10)

    @staticmethod
    def user_payload():
        password = DataGenerator.password()
        return {
        "email": DataGenerator.email(),
        "fullName": DataGenerator.name(),
        "password": password,
        "passwordRepeat": password
    }

    @staticmethod
    def name_movie():
        return fake.lexify(text='??????? ?????')

    @staticmethod
    def movie_payload(genre_id):
        location = ['SPB', 'MSK']

        return {
            "name": fake.catch_phrase(),
            "imageUrl": fake.image_url(),
            "price": fake.random_int(min=1,max=1000),
            "description": fake.paragraph(nb_sentences=4),
            "location": fake.random_element(location),
            "published": True,
            "genreId": genre_id,
}

    @staticmethod
    def random_pagesize():
        return fake.random_int(min=2, max=20)

    @staticmethod
    def random_page():
        return fake.random_int(min=1, max=2)

    @staticmethod
    def random_created_at():
        created_at = ['asc', 'desc']
        return fake.random_element(created_at)

    @staticmethod
    def random_big_int():
        return fake.random_int(min=99999, max=999999)
