from src.models import AuthAdmin



class AuthAdminService():

    def __init__(self):
        self.__auth = AuthAdmin()


    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

