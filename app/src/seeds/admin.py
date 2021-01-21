from faker import Faker
from src.models import Admin 

faker = Faker() 

class AdminSeed():
    __seed__ = 'admin'

    def __init__(self):
        self.__model = Admin(
                display_name=faker.profile()['username'],
                email=faker.email(),
                password=faker.password(),
                phone_number=faker.phone_number(),
                photo_url=faker.image_url(),
                name=faker.first_name(),
                lastname=faker.last_name(),
                disabled=False)  
    
    def run(self):
        self.__model.create_user()
        self.__model.save();
