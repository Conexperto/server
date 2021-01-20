from src.models import Auth



class AuthService():

    def __init__(self):
        self.__auth = Auth()


    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

    
    def create_user(self, user, body):
        pass

    def update_user(self, user, body):
        pass

    def update_field_user(self, user, body):
        pass

    def delete_user(self, user, body):
        pass

    def response(self):
        return self.response
