from src.models import Auth, User



class AuthService():

    def __init__(self):
        self.__auth = Auth()


    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

    
    def create_user(self, body):
        user_record = self.__auth.create_user(
                        email=body['email'],
                        password=body['password'],
                        display_name=body['display_name'])
        
        user = User(uid=user_record.uid,
                        email=body['email'],
                        display_name=body['display_name'])
        
        user.add()
        user.save()

        return user

    def update_user(self, user, body):
        pass

    def update_field_user(self, user, body):
        pass

    def delete_user(self, user, body):
        pass

