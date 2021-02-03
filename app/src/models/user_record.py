from flask import abort
from firebase_admin import auth



class UserRecord():

    @staticmethod
    def verify_id_token(id_token, check_revoked, app):
        try:
            return auth.verify_id_token(id_token, check_revoked=check_revoked, app=app)
        except auth.ExpiredIdTokenError as ex:
            raise abort(401, description='ExpiredIdToken')
        except auth.InvalidIdTokenError as ex:
            raise abort(401, description='InvalidIdToken')
        except auth.RevokedIdTokenError as ex:
            raise abort(401, description='RevokedIdToken')
        except auth.TokenSignError as ex:
            raise abort(401, description='TokenSign')
        except auth.UnexpectedResponseError as ex:
            raise abort(500, description='UnexpectedResponse')


    @classmethod
    def get_user(cls, uid, app):
        try:
            return cls(auth.get_user(uid, app=app), app=app)
        except auth.UserNotFoundError as ex:
            raise abort(404, description='UserNotFound')
        except auth.UnexpectedResponseError as ex:
            raise abort(500, description='UnexpectedResponse')

    @classmethod
    def create_user(cls, email, password, display_name, app):
        try:
            return cls(auth.create_user(
                                email=email,
                                password=password,
                                display_name=display_name, app=app), app=app)
        except auth.UidAlreadyExistsError as ex:
            raise abort(400, description='UidAlreadyExists')
        except auth.EmailAlreadyExistsError as ex:
            raise abort(400, description='EmailAlreadyExists', response='auth/email-already-in-use')
        except auth.PhoneNumberAlreadyExistsError as ex:
            raise abort(400, description='PhoneNumberAlreadyExists')
        except auth.UnexpectedResponseError as ex:
            raise abort(500, description='UnexpectedResponse')

    def __init__(self, user_record, app):
        self.app = app

        self.uid = user_record.uid
        self.email = user_record.email
        self.email_verified = user_record.email_verified
        self.display_name = user_record.display_name
        self.phone_number = user_record.phone_number
        self.photo_url = user_record.photo_url
        self.disabled = user_record.disabled
        self.provider_data = [
            {
                'uid': provider.uid,
                'display_name': provider.display_name,
                'email': provider.email,
                'phone_number': provider.phone_number,
                'photo_url': provider.photo_url,
                'provider_id': provider.provider_id
            } for provider in user_record.provider_data
        ]
        self.custom_claims = user_record.custom_claims
        self.tokens_valid_after_timestamp = user_record.tokens_valid_after_timestamp

    def update_user(self):
        try:
            auth.update_user(
                    uid=self.uid,
                    email=self.email,
                    password=self.password,
                    display_name=self.display_name,
                    phone_number=self.phone_number,
                    photo_url=self.photo_url,
                    disabled=self.disabled, app=self.app)
        except auth.UidAlreadyExistsError as ex:
            raise abort(400, description='UidAlreadyExists')
        except auth.EmailAlreadyExistsError as ex:
            raise abort(400, description='EmailAlreadyExists')
        except auth.PhoneNumberAlreadyExistsError as ex:
            raise abort(400, description='PhoneNumberAlreadyExists')
        except auth.UnexpectedResponseError as ex:
            raise abort(500, description='UnexpectedResponse')

    def delete_user(self):
        try:
            auth._delete_user(uid=self.uid, app=self.app)
        except auth.UserNotFoundError as ex:
            raise abort(404, description='UserNotFound')
        except auth.UnexpectedResponseError as ex:
            raise abort(500, description='UnexpectedResponse')

    def make_claims(self, claims={}):
        try:
            auth.set_custom_user_claims(self.uid, claims, app=self.app)
        except auth.UserNotFoundError as ex:
            raise abort(404, description='UserNotFound')
        except auth.UnexpectedResponseError as ex:
            raise abort(500, description='UnexpectedResponse')
    
    def serialize(self, obj):
        for key, val in obj.items():
            if key in self.keys():
                self[key] = val
        return self
