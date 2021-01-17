from flask_script import Command
from faker import Faker
from src.models import TestModel

faker = Faker() 

class TestSeed(Command, TestModel):

    def __init__(self):
        self.name = faker.name();  
    
    def run(self):
        self.save();
