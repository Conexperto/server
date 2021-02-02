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
        postgres_user = user['b']

        if(postgres_user.display_name != body['display_name']):
            postgres_user.display_name = body['display_name']

        if(postgres_user.email != body['email']):
            postgres_user.email = body['email']

        if(postgres_user.phone_number != body['phone_number']):
            postgres_user.phone_number = body['phone_number']

        if(postgres_user.photo_url != body['photo_url']):
            postgres_user.photo_url = body['photo_url']

        if(postgres_user.photo_url != body['name']):
            postgres_user.name = body['name']

        if(postgres_user.lastname != body['lastname']):
            postgres_user.lastname = body['lastname']

        if(postgres_user.headline != body['headline']):
            postgres_user.headline = body['headline']

        if(postgres_user.about_me != body['about_me']):
            postgres_user.about_me = body['about_me']

        if(postgres_user.timezone != body['timezone']):
            postgres_user.timezone = body['timezone']

        postgres_user.save()

        return { 'a': firebase_user, 'b': postgres_user }

    def update_field_user(self, user, body):
        pass

    def delete_user(self, user, body):
        pass

