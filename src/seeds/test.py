""" src.seeds.test """
from faker import Faker
from src.models import TestModel

faker = Faker()


class TestSeed:
    """
    TestSeed
    """

    __seed__ = "test"

    def __init__(self):
        self.__model = TestModel(name=faker.name())

    def run(self):
        """run"""
        self.__model.add()
        self.__model.save()
