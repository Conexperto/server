""" src.seeds.admin """
from faker import Faker

from src.models import Admin
from src.models import Privileges


faker = Faker()


class AdminSeed:
    """
    AdminSeed
    """

    __seed__ = "admin"

    def __init__(self):
        self.__model = Admin(
            uid="VaAJS4ag2hgUnDunBEM9Xxf83ZJ2",
            display_name="conexpertotesting",
            email="conexpertotesting@gmail.com",
            phone_number="+10000000000",
            photo_url=faker.image_url(),
            name="conexpertotesting",
            lastname="conxpertotesting",
            disabled=False,
            privilegies=Privileges.SuperRoot.value,
        )

    def run(self):
        """run"""
        self.__model.add()
        self.__model.save()
