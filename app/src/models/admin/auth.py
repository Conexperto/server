from werkzeug.exceptions import Unauthorized
from firebase_admin import auth
from src.firebase import admin_sdk



class AuthAdminModel():

    def __init__(self):
        pass

    def authentication(self, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token, check_revoked=True, app=admin_sdk)
            user_record = auth.get_user(decoded_token['uid'], app=admin_sdk)
            
            claims = user_record.custom_claims
            
            #auth.set_custom_user_claims(decoded_token['uid'], { 'admin': True, 'access_level': 0 }, app=admin_sdk)

            if not claims:
                raise Unauthorized('Úser is not admin')

            if not claims['admin']:
                raise Unauthorized('User is not admin')

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
                'b': {

                }
            }

        except auth.RevokedIdTokenError as ex:
            raise Unauthorized('Revoked Token!!')
        except auth.ExpiredIdTokenError as ex:
            raise Unauthorized('Expired Token!!')
        except auth.InvalidIdTokenError as ex:
            raise Unauthorized('Invalid Token!!')



