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

    def get_userById(self, body):
        user = User.query.filter_by(id=body['id']).first()
        return user

    def get_userByUid(self, body):
        user = User.query.filter_by(uid=body['uid']).first()
        return user

    def get_userByEmail(self, body):
        user = User.query.filter_by(email=body['email']).first()
        return user

    def update_user(self, user, body):
        user = user['b']
        # insert changes 

        if(user.display_name != body['display_name']):
            user.display_name = body['display_name']

        user.save()

        return user

    def update_field_user(self, user, body):
        pass

    def delete_user(self, user, body):
        pass

