from faker import Faker

faker = Faker()

BASE_USER_PASSWORD = "USER1234$123"


def generate_user_credentials() -> dict:
    return {
        "email": faker.email(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": BASE_USER_PASSWORD,
    }
