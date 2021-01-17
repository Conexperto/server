from werkzeug.exceptions import Unauthorized
from firebase_admin import auth
from src.firebase import admin_sdk



class AuthAdminModel():

    def __init__(self):
        pass

    def authentication(self, id_token):
        try:
            decoded_token = auth.verify_id_token(id_token, check_revoked=True, app=admin_sdk)
            user_record = auth.get_user(decoded_token, app=admin_sdk)
            
            claims = user_record['customClaims']

            if not claims['admin']:
                raise Unauthorized('User is not admin')

            if not user_record['disabled']:
                raise Unauthorized('Account disabled')

            return {
                'uid': user_record['uid'],
                'a': {
                    'uid': userRecord['uid'],
                    'email': userRecord['email'],
                    'emailVerified': userRecord['emailVerified'],
                    'displayName': userRecord['displayName'],
                    'phoneNumber': userRecord['phoneNumber'],
                    'photoURL': userRecord['photoURL'],
                    'disabled': userRecord['disabled'],
                    'providerData': userRecord['providerData'],
                    'customClaims': userRecord['customClaims'],
                    'tokensValidAfterTime': userRecord['tokensValidAfterTime']
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



