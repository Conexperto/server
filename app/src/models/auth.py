from werkzeug.exceptions import Unauthorized, BadRequest, NotFound, InternalServerError
from firebase_admin import auth
from src.firebase import web_sdk
from .user import User


class UserRecord():

    @staticmethod
    def verify_id_token(id_token, check_revoked):
        try:
            return auth.verify_id_token(id_token, check_revoked=check_revoked, app=web_sdk)
        except auth.ExpiredIdTokenError as ex:
            raise Unauthorized('ExpiredIdToken')
        except auth.InvalidIdTokenError as ex:
            raise Unauthorized('InvalidIdToken')
        except auth.RevokedIdTokenError as ex:
            raise Unauthorized('RevokedIdToken')
        except auth.TokenSignError as ex:
            raise Unauthorized('TokenSign')
        except auth.UnexpectedResponseError as ex:
            raise Unauthorized('UnexpectedResponse')


    @classmethod
    def get_user(cls, uid):
        try:
            return cls(auth.get_user(uid, app=web_sdk))
        except auth.UserNotFoundError as ex:
            raise NotFound('UserNotFound')
        except auth.UnexpectedResponseError as ex:
            raise InternalServerError('UnexpectedResponse')

    @classmethod
    def create_user(cls, body):
        try:
            return cls(auth.create_user(body, app=web_sdk))
        except auth.UidAlreadyExistsError as ex:
            raise BadRequest('UidAlreadyExists')
        except auth.EmailAlreadyExistsError as ex:
            raise BadRequest('EmailAlreadyExists')
        except auth.PhoneNumberAlreadyExistsError as ex:
            raise BadRequest('PhoneNumberAlreadyExists')
        except auth.UnexpectedResponseError as ex:
            raise InternalServerError('UnexpectedResponse')

    def __init__(self, user_record):
        self.uid: user_record.uid
        self.email: user_record.email
        self.email_verified: user_record.email_verified
        self.display_name: user_record.display_name
        self.phone_number: user_record.phone_number
        self.photo_url: user_record.photo_url
        self.disabled: user_record.disabled
        self.provider_data: [
            {
                'uid': provider.uid,
                'displayName': provider.display_name,
                'email': provider.email,
                'phoneNumber': provider.phone_number,
                'photoURL': provider.photo_url,
                'providerId': provider.provider_id
            } for provider in user_record.provider_data
        ]
        self.customClaims: user_record.custom_claims
        self.tokensValidAfterTime: user_record.tokens_valid_after_timestamp

    def update_user(self):
        try:
            auth.update_user(
                    uid=self.uid,
                    email=self.email,
                    password=self.password,
                    display_name=self.display_name,
                    phone_number=self.phone_number,
                    photo_url=self.photo_url,
                    disabled=self.disabled, app=web_sdk)
        except auth.UidAlreadyExistsError as ex:
            raise BadRequest('UidAlreadyExists')
        except auth.EmailAlreadyExistsError as ex:
            raise BadRequest('EmailAlreadyExists')
        except auth.PhoneNumberAlreadyExistsError as ex:
            raise BadRequest('PhoneNumberAlreadyExists')
        except auth.UnexpectedResponseError as ex:
            raise InternalServerError('UnexpectedResponse')

    def delete_user(self):
        try:
            auth._delete_user(uid=self.uid, app=web_sdk)
        except auth.UserNotFoundError as ex:
            raise NotFound('UserNotFound')
        except auth.UnexpectedResponseError as ex:
            raise InternalServerError('UnexpectedResponse')

    def make_claims(self, complete_register):
        try:
            auth.set_custom_user_claims(self.uid, { 'complete_register': complete_register }, app=web_sdk)
        except auth.UserNotFoundError as ex:
            raise NotFound('UserNotFound')
        except auth.UnexpectedResponseError as ex:
            raise InternalServerError('UnexpectedResponse')
    
    def serialize(self, obj):
        for key, val in obj.items():
            if key in self.keys():
                self[key] = val

class Auth():

    def authentication(self, id_token):
        decoded_token = UserRecord.verify_id_token(id_token, check_revoked=True)
        user_record = UserRecord.get_user(decoded_token['uid'])

        if user_record.disabled:
            raise Unauthorized('AccountDisabled')
        
        user = User.query.filter_by(uid=user_record.uid).first()

        return {
            'uid': user_record.uid,
            'a': user_record,
            'b': user
        }
