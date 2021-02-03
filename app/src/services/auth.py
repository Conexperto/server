from src.models import Auth, UserRecord, User



class AuthService():

    def __init__(self):
        self.__auth = Auth()


    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

    def create_user(self, body):
        user_record = UserRecord.create_user(
                        email=body['email'],
                        password=body['password'],
                        display_name=body['display_name'])
        user_record.custom_claims({ 'complete_register': False })
        
        user = User(uid=user_record.uid,
                        email=body['email'],
                        display_name=body['display_name'])
        user.add()
        user.save()

        return { 
            'uid': user_record.uid,
            'a': user_record, 
            'b': user 
        }

    def update_user(self, user, body):
        user_record = user['a']
        _user = user['b']
       
        user_record.serialize(body)
        user_record.update_user()
        user_record.custom_claims({ 'complete_register': True })

        _user.serialize(body)
        _user.save()  

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': _user
        } 

    def update_field_user(self, user, body):
        user_record = user['a']
        _user = user['b']
       
        user_record.serialize(body)
        user_record.update_user()

        _user.serialize(body)
        _user.save()  

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': _user
        } 

    def delete_user(self, user):
        user_record = user['a']
        _user = user['b']

        user_record.delete_user()
        _user.delete()
        

