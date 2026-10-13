

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
        return fake.first_name()

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
    def name_cinema():
        return fake.catch_phrase()

    @staticmethod
    def cinema_payload(genre_id):
        location = ['SPB', 'MSK']
        return {
            "name": fake.catch_phrase(),
            "imageUrl": fake.image_url(),
            "price": fake.random_int(min=1,max=9999),
            "description": fake.paragraph(nb_sentences=4),
            "location": fake.random_element(location),
            "published": fake.boolean(),
            "genreId": genre_id
}





