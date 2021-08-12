""" src.seeds.speciality """
from faker import Faker

from src.models import Speciality

faker = Faker()


class SpecialitySeed:
    """
    SpecialitySeed
    """

    __seed__ = "speciality"

    def __init__(self):
        self.__model = Speciality(name=faker.job())

    def run(self):
        """run"""
        self.__model.add()
        self.__model.save()
