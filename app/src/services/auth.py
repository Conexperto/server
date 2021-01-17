from src.models import AuthModel



class AuthService():

    def __init__(self):
        self.__auth = AuthModel()


    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

