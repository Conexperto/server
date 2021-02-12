from flask import abort
from firebase_admin import auth
from src.firebase import web_sdk
from .user_record import UserRecord
from .user import User


class Auth():

    def authentication(self, id_token):
        decoded_token = UserRecord.verify_id_token(id_token, check_revoked=True, app=web_sdk)
        user_record = UserRecord.get_user(decoded_token['uid'], app=web_sdk)
        
        if user_record.disabled:
            raise abort(401, description='AccountDisabled', response='auth/account-disabled')
    
        claims = user_record.custom_claims;
    
        user = User.query.filter_by(uid=user_record.uid).first()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }
