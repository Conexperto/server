""" seeds.method.py """
from faker import Faker
from src.models import Method

faker = Faker()


class MethodSeed:
    """MethodSeed"""

    __seed__ = "method"

    def __init__(self):
        self.__model = Method(name=faker.domain_word())

    def run(self):
        """run"""
        self.__model.add()
        self.__model.save()
