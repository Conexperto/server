from src.models.admin import AuthAdminModel



class AuthAdminService():

    def __init_(self):
        self.__auth = AuthAdminModel()


    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

