from faker import Faker
from src.models import Method

faker = Faker()

class MethodSeed():
    __seed__ = 'method'

    def __init__(self):
        self.__model = Method(name=faker.domain_word())

    def run(self):
        self.__model.save()
