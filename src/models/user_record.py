"""
    Model: UserRecord
"""
from firebase_admin import auth as _auth

from src.exceptions import HandlerException
from src.mixins import Record


class UserRecord(Record):
    """
    The UserRecord is a small abstraction layer to use firebase-admin auth.

    Args:
        user_record (UserRecord): Instance of UserRecord
        auth (firebase.auth.Client): firebase.auth.Client

    Attribues:
        auth (firebase.auth.Client): Instance of firebase auth client
        uid (str): User uid
        email (str): User email
        email_verified (bool): User verification status
        password (str): User password
        display_name (str): User display_name
        phone_number (str): User phone number
        photo_url (str): User photo_url
        disabled (bool): User status
        provider_data (list):
            uid (str): Provider uid
            display_name (str): User display name
            email (str): User email
            phone_number (str): User phone number
            photo_url (str): User photo url
            provider_id (str): Provider identifier
        custom_claims (dict): Contains session claims
        tokens_valid_after_timestamp (str): token deadline
    """

    @staticmethod
    def verify_id_token(id_token, check_revoked, auth):
        """
        Returns decoded token

            Args:
                id_token (str): jwt generate by client/firebase
                check_revoked (bool): Check if token is revoked
                app (firebase.auth.Client): firebase.auth.Client

            Raises:
                ExpiredIdTokenError: The passed token is expired
                RevokedIdTokenError: The passed token is revoked
                InvalidIdTokenError: The passed token is invalid
                TokenSignError: The passed token has sign errors

            Returns:
                decoded_token
        """
        try:
            return auth.verify_id_token(id_token)
        except _auth.ExpiredIdTokenError as ex:
            raise HandlerException(401, "Expired IdToken", str(ex))
        except _auth.RevokedIdTokenError as ex:
            raise HandlerException(401, "Revoked IdToken", str(ex))
        except _auth.InvalidIdTokenError as ex:
            raise HandlerException(401, "Invalid IdToken", str(ex))
        except _auth.TokenSignError as ex:
            raise HandlerException(401, "Token sign", str(ex))
        except _auth.UnexpectedResponseError as ex:
            raise HandlerException(500, "Unexpected response", str(ex))

    @classmethod
    def get_user(cls, uid, auth):
        """
        Returns data user

            Args:
                uid (str): user uid
                auth (firebase.auth.Client): firebase.auth.Client

            Raises:
               UserNotFoundError: Not found user by uid

            Returns:
                UserRecord
        """
        try:
            return cls(auth.get_user(uid), auth)
        except _auth.UserNotFoundError as ex:
            raise HandlerException(404, "User not found", str(ex))
        except _auth.UnexpectedResponseError as ex:
            raise HandlerException(500, "Unexpected response", str(ex))

    @classmethod
    def create_user(cls, auth, **kwargs):
        """
        Returns data user created

            Args:
                auth (firebase.auth.Client): firebase.auth.Client
                email (str): Email of user
                password (str): Password of user
                display_name (str): Display name of user

            Raises:
                EmailAlreadyExistsError: Email already exists
                PhoneNumberAlreadyExistsError: Phone number already exists

            Returns:
                UserRecord
        """
        try:
            return cls(
                auth.create_user(**kwargs),
                auth,
            )
        except _auth.EmailAlreadyExistsError as ex:
            raise HandlerException(400, "Email already exists", str(ex))
        except _auth.PhoneNumberAlreadyExistsError as ex:
            raise HandlerException(400, "PhoneNumber already exists", str(ex))
        except _auth.UnexpectedResponseError as ex:
            raise HandlerException(500, "Unexpected response", str(ex))

    def __init__(self, user_record, auth):
        self.auth = auth
        self.uid = user_record.uid
        self.email = user_record.email
        self.email_verified = user_record.email_verified
        self.password = (
            user_record.password if hasattr(user_record, "password") else None
        )
        self.display_name = user_record.display_name
        self.phone_number = user_record.phone_number
        self.photo_url = user_record.photo_url
        self.disabled = user_record.disabled
        self.provider_data = [
            {
                "uid": provider.uid,
                "display_name": provider.display_name,
                "email": provider.email,
                "phone_number": provider.phone_number,
                "photo_url": provider.photo_url,
                "provider_id": provider.provider_id,
            }
            for provider in user_record.provider_data
        ]
        self.custom_claims = user_record.custom_claims
        self.tokens_valid_after_timestamp = (
            user_record.tokens_valid_after_timestamp
        )

    def update_user(self):
        """
        Update user fields

        Raises:
            EmailAlreadyExistsError: Email already exists
            PhoneNumberAlreadyExistsError: Phone number already exists
        """
        try:
            _repr_hide = [
                "auth",
                "provider_data",
                "custom_claims",
                "tokens_valid_after_timestamp",
            ]

            args = {}
            for k, v in self.__dict__.items():
                if k in _repr_hide:
                    continue
                if v is None:
                    continue
                args[k] = v

            self.auth.update_user(**args)
        except _auth.EmailAlreadyExistsError as ex:
            raise HandlerException(400, "Email already exists", str(ex))
        except _auth.PhoneNumberAlreadyExistsError as ex:
            raise HandlerException(400, "PhoneNumber already exists", str(ex))
        except _auth.UnexpectedResponseError as ex:
            raise HandlerException(500, "Unexpected response", str(ex))

    def delete_user(self):
        """
        Delete user by uid

        Raises:
           UserNotFoundError: Not found user by uid
        """
        try:
            self.auth.delete_user(uid=self.uid)
        except _auth.UserNotFoundError as ex:
            raise HandlerException(404, "User not found", str(ex))
        except _auth.UnexpectedResponseError as ex:
            raise HandlerException(500, "Unexpected response", str(ex))

    def make_claims(self, claims=None):
        """
        Make claims

        Args:
            claims (dict): Contains all claims

        Raises:
           UserNotFoundError: Not found user by uid
        """
        try:
            self.auth.set_custom_user_claims(self.uid, claims or {})
        except _auth.UserNotFoundError as ex:
            raise HandlerException(404, "User not found", str(ex))
        except _auth.UnexpectedResponseError as ex:
            raise HandlerException(500, "Unexpected response", str(ex))
