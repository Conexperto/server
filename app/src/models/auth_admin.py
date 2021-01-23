from werkzeug.exceptions import Unauthorized
from .admin import Admin
from firebase_admin import auth
from src.firebase import admin_sdk



class AuthAdmin():

    def __init__(self):
        pass

    def authentication(self, id_token):
        try:
            decoded_token = self.verify_id_token(id_token, check_revoked=True, app=admin_sdk)
            user_record = self.get_user(decoded_token['uid'], app=admin_sdk)
            
            claims = user_record.custom_claims

            if not claims:
                raise Unauthorized('User is not admin')

            if not claims['admin']:
                raise Unauthorized('User is not admin')

            if user_record.disabled:
                raise Unauthorized('Account disabled')
    
            user = Admin.query.filter_by(uid=uid).first()

            return {
                'uid': user_record.uid,
                'a': {
                    'uid': user_record.uid,
                    'email': user_record.email,
                    'emailVerified': user_record.email_verified,
                    'displayName': user_record.display_name,
                    'phoneNumber': user_record.phone_number,
                    'photoURL': user_record.photo_url,
                    'disabled': user_record.disabled,
                    'providerData': [
                        {
                            'uid': provider.uid,
                            'display_name': provider.display_name,
                            'email': provider.email,
                            'phone_number': provider.phone_number,
                            'photo_url': provider.photo_url,
                            'provider_id': provider.provider_id
                        } for provider in user_record.provider_data
                    ],
                    'customClaims': user_record.custom_claims,
                    'tokensValidAfterTime': user_record.tokens_valid_after_timestamp
                },
                'b': user
            }

        except auth.RevokedIdTokenError as ex:
            raise Unauthorized('Revoked Token!!')
        except auth.ExpiredIdTokenError as ex:
            raise Unauthorized('Expired Token!!')
        except auth.InvalidIdTokenError as ex:
            raise Unauthorized('Invalid Token!!')

    def get_user(self, uid):
        return auth.get_user(uid, app=admin_sdk)

    def verify_id_token(self, id_token, check_revoked):
        return auth.verify_id_token(id_token, check_revoked=check_revoked, app=admin_sdk)

    def create_user(self, email, password, display_name):
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name, app=admin_sdk)

        return user

    def update_user(self, uid, email, password, display_name, phone_number, photo_url, disabled):
        return auth.update_user(
                uid=uid,
                email=email,
                password=password,
                display_name=display_name,
                phone_number=phone_number,
                photo_url=photo_url,
                disabled=disabled, app=admin_sdk)

    def disabled_user(self, uid, disabled):
        return auth.update_user(
                uid=uid, 
                disabled= not disabled, app=admin_sdk)

    def delete_user(self):
        auth.delete_user(uid=uid, app=admin_sdk)

    def make_claims(self, privilegies):
        auth.set_custom_user_claims(
                uid,
                { 'admin': True, 'access_level': privilegies }, app=admin_sdk)
