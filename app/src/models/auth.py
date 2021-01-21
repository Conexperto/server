from werkzeug.exceptions import Unauthorized
from firebase_admin import auth
from src.firebase import web_sdk
from .user import User



class Auth():

    def __init__(self):
        pass

    def authentication(self, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token, check_revoked=True, app=web_sdk)
            user_record = auth.get_user(decoded_token['uid'], app=web_sdk)

            if user_record.disabled:
                raise Unauthorized('Account disabled')
            
            

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
                'b': {

                }
            }

        except auth.RevokedIdTokenError as ex:
            raise Unauthorized('Revoked Token!!')
        except auth.ExpiredIdTokenError as ex:
            raise Unauthorized('Expired Token!!')
        except auth.InvalidIdTokenError as ex:
            raise Unauthorized('Invalid Token!!')



