from src.models import AuthAdmin, UserRecord, Admin, Privilegies



class AuthAdminService():

    def __init__(self):
        self.__auth = AuthAdmin()


    def authentication(self, id_token):
        return self.__auth.authentication(id_token)
    
    def create_user(self, body):
        user_record = UserRecord.create_user(
                        email=body['email'],
                        password=body['password'],
                        display_name=body['display_name'])
        user_record.custom_claims({ 
            'admin': True, 
            'access_level': Privilegies.User.value })
        
        user = Admin(uid=user_record.uid,
                        display_name=body['display_name'],
                        email=body['email'],
                        phone_number=body['phone_number'],
                        name=body['name'],
                        lastname=body['lastname'],
                        privilegies=body['privilegies'])
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

        if 'privilegies' in body and not body['privilegies']:
            user_record.custom_claims({ 'access_level': body['privilegies'] })

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

        if 'privilegies' in body and not body['privilegies']:
            user_record.custom_claims({ 'access_level': body['privilegies'] })

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
        

