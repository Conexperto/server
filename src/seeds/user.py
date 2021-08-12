""" src.seeds.user """
from faker import Faker

from src.models import User

faker = Faker()


class UserSeed:
    """
    UserSeed
    """

    __seed__ = "user"

    def __init__(self):
        self.__model = User(
            uid="bdqSmcPYhUZZn3Kxg3vcIuKP4Rs1",
            display_name="conexpertotesting",
            email="conexpertotesting@gmail.com",
            phone_number="+10000000000",
            photo_url=faker.image_url(),
            name="conexpertotesting",
            lastname="conexpertotesting",
            disabled=False,
            headline=faker.text(max_nb_chars=50),
            about_me=faker.text(max_nb_chars=100),
            complete_register=True,
        )

    def run(self):
        """run"""
        self.__model.add()
        self.__model.save()
