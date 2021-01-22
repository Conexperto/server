from faker import Faker
from src.models import Admin, Privilegies 
from firebase_admin import auth


faker = Faker() 

class AdminSeed():
    __seed__ = 'admin'

    def __init__(self):
        self.__model = Admin(
                uid='VaAJS4ag2hgUnDunBEM9Xxf83ZJ2', 
                display_name='conexpertotesting',
                email='conexpertotesting@gmail.com',
                phone_number='+10000000000',
                photo_url=faker.image_url(),
                name='conexpertotesting',
                lastname='conxpertotesting',
                disabled=False,
                privilegies=Privilegies.SuperRoot.value)  
    
    def run(self):
        self.__model.save()
