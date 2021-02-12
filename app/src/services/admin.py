from flask import abort
from src.models import UserRecord, Admin 
from src.firebase import admin_sdk
from src.models import Privilegies



class AdminService:

    def get(self, uid):
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def list(self, page=1, per_pages=10):
        users = Admin.query.paginate(page, per_pages or 10, error_out=False)
       
        return users

    def create(self, body):
        try:
            user_record = UserRecord(
                    email=body['email'],
                    password=body['password'],
                    display_name=body['display_name'],
                    phone_number=body['phone_number'], app=admin_sdk)

            user_record.make_claims({ 
                            'admin': True, 
                            'access_level': body['privilegies'] if hasattr(body, 'privilegies') else Privilegies.User.value })
            
            user = Admin(uid=user_record.uid,
                            email=body['email'],
                            display_name=body['display_name'],
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
        except KeyError as ex:
            abort(400, description='BadRequest', response=str(ex))

    def update(self, uid, body):
        user_record = UserRecord.get_user(uid, app=admin_sdk) 
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize(body)
        user_record.update_user()
    
        if hasattr(body, 'privilegies'):
            user_record.make_claims({ 
                        'admin': True, 
                        'access_level': body['privilegies'] })

        user.serialize(body)
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def update_field(self, uid, body):
        user_record = UserRecord.get_user(uid, app=admin_sdk) 
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize(body)
        user_record.update_user()
        
        if hasattr(body, 'privilegies'):
            user_record.make_claims({ 
                        'admin': True, 
                        'access_level': body['privilegies'] })

        user.serialize(body)
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def disabled(self, uid):
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.serialize({ 'disabled': not user_record.disabled })
        user_record.update_user()

        user.serialize({ 'disabled': not user_record.disabled })
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }


    def delete(self, uid):
        user_record = UserRecord.get_user(uid, app=admin_sdk)
        user = Admin.query.filter_by(uid=user_record.uid).first()

        if not user_record or not user:
            abort(404, description='NotFound', response='not_found')

        user_record.delete_user()
        user.delete()

        return {
            'uid': user_record.uid
        }

