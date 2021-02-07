from src.models import UserRecord, User
from src.firebase import web_sdk


class UserService:

    def get_user(self, uid):
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def list_user(self, page=1):
        per_pages = 10
        users = User.query.paginate(page, per_pages, error_out=False)
        
        return users

    def create_user(self, body):
        user_record = UserRecord(
                email=body['email'],
                password=body['password'],
                display_name=body['display_name'],
                phone_number=body['phone_number'], app=web_sdk)
        user_record.make_claims({ 'complete_register': body['complete_register'] if hasattr(body, 'complete_register') else False })
        
        user = User(uid=user_record.uid,
                        email=body['email'],
                        display_name=body['display_name'],
                        phone_number=body['phone_number'],
                        name=body['name'],
                        lastname=body['lastname'],
                        headline=body['headline'],
                        about_me=body['about_me'],
                        complete_register=body['complete_register'] if hasattr(body, 'complete_register') else False)

        user.add()
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def update_user(self, uid, body):
        user_record = UserRecord.get_user(uid, app=web_sdk) 
        user = User.query.filter_by(uid=user_record.uid).first()

        user_record.serialize(body)
        user_record.update_user()
        
        user_record.make_claims({ 'complete_register' : hasattr(body, 'complete_register') if body['complete_register'] else False })

        user.serialize(body)
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def update_field_user(self, uid, body):
        user_record = UserRecord.get_user(uid, app=web_sdk) 
        user = User.query.filter_by(uid=user_record.uid).first()

        user_record.serialize(body)
        user_record.update_user()
        
        user_record.make_claims({ 'complete_register' : hasattr(body, 'complete_register') if body['complete_register'] else False })

        user.serialize(body)
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }

    def disabled_user(self, uid):
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        user_record.serialize({ 'disabled': not user_record.disabled })
        user_record.update_user()

        user.serialize({ 'disabled': not user_record.disabled })
        user.save()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }


    def delete_user(self, uid):
        user_record = UserRecord.get_user(uid, app=web_sdk)
        user = User.query.filter_by(uid=user_record.uid).first()

        user_record.delete_user()
        user.delete()

        return {
            'uid': user_record.uid
        }
