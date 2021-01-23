from werkzeug.exceptions import Unauthorized
from firebase_admin import auth
from src.firebase import web_sdk
from .user import User



class Auth():

    def __init__(self):
        pass

    def authentication(self, id_token):
        try:
            decoded_token = self.verify_id_token(id_token, check_revoked=True)
            user_record = self.get_user(decoded_token['uid'])

            if user_record.disabled:
                raise Unauthorized('Account disabled')
            
            user = User.query.filter_by(uid=user_record.uid).first()

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
                            'displayName': provider.display_name,
                            'email': provider.email,
                            'phoneNumber': provider.phone_number,
                            'photoURL': provider.photo_url,
                            'providerId': provider.provider_id
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
        return auth.get_user(uid, app=web_sdk)

    def verify_id_token(self, id_token, check_revoked):
        return auth.verify_id_token(id_token, check_revoked=check_revoked, app=web_sdk)

    def create_user(self, email, password, display_name):
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name, app=web_sdk)

        return user

    def update_user(self, uid, email, password, display_name, phone_number, photo_url, disabled):
        user = auth.update_user(
                uid=uid,
                email=email,
                password=password,
                display_name=display_name,
                phone_number=phone_number,
                photo_url=photo_url,
                disabled=disabled, app=web_sdk)
        
        return user

    def delete_user(self, uid):
        auth._delete_user(uid=uid, app=web_sdk)

    def make_claims(self, uid, complete_register):
        auth.set_custom_user_claims(
                uid, { 'complete_register': complete_register }, app=web_sdk)

