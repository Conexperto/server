from flask import abort
from src.models import AuthAdmin, UserRecord, Admin, Privilegies
from src.firebase import admin_sdk



class AuthAdminService():

    def __init__(self):
        self.__auth = AuthAdmin()

    def authentication(self, id_token):
        return self.__auth.authentication(id_token)
    
    def create(self, body):
        try:
            user = {
                'email': body['email'],
                'password': body['password'],
                'display_name': body['display_name']
            }
            user_record = UserRecord.create_user(user, app=admin_sdk)
            user_record.make_claims({ 
                'admin': True, 
                'access_level': body['privilegies'] if hasattr(body, 'privilegies') else Privilegies.User.value })
            
            user = Admin(uid=user_record.uid,
                            display_name=body['display_name'],
                            email=body['email'],
                            phone_number=body['phone_number'],
                            name=body['name'],
                            lastname=body['lastname'],
                            privilegies=body['privilegies'] or Privilegies.User.value)
            user.add()
            user.save()

            return { 
                'uid': user_record.uid,
                'a': user_record, 
                'b': user 
            }
        except KeyError as ex:
            abort(400, description='BadRequest', response=str(ex))

    def update(self, user, body):
        user_record = user['a']
        _user = user['b']

        if not user_record or not _user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize(body)
        user_record.update_user()
        
        if hasattr(body, 'privilegies') and not body['privilegies']:
            user_record.make_claims({ 'access_level': body['privilegies'] })

        _user.serialize(body)
        _user.save()  

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': _user
        } 

    def update_field(self, user, body):
        user_record = user['a']
        _user = user['b']

        if not user_record or not _user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize(body)
        user_record.update_user()

        if hasattr(body, 'privilegies') and not body['privilegies']:
            user_record.make_claims({ 'access_level': body['privilegies'] })

        _user.serialize(body)
        _user.save()  

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': _user
        } 

    def disabled(self, user):
        user_record = user['a']
        _user = user['b']

        if not user_record or not _user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize({ 'disabled': not user_record.disabled })
        user_record.update_user()

        user.serialize({ 'disabled': not user_record.disabled })
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': _user
        }

    def delete(self, user):
        user_record = user['a']
        _user = user['b']

        if not user_record or not _user:
            abort(404, description='NotFound', response='not_found')

        user_record.delete_user()
        _user.delete()
        

