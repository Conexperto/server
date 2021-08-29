from flask import abort

from src.firebase import web_sdk
from src.models import Auth
from src.models import User
from src.models import UserRecord
from src.services.expert import ExpertService


class AuthService:
    def __init__(self):
        self.__auth = Auth()

    def authentication(self, id_token):
        return self.__auth.authentication(id_token)

    def create(self, body):
        try:
            user = {
                "email": body["email"],
                "password": body["password"],
                "display_name": body["display_name"],
            }
            user_record = UserRecord.create_user(user, app=web_sdk)
            user_record.make_claims({"complete_register": False})

            user = User(
                uid=user_record.uid,
                email=body["email"],
                display_name=body["display_name"],
            )
            user.add()
            user.save()

            return {"uid": user_record.uid, "a": user_record, "b": user}
        except KeyError as ex:
            abort(400, description="BadRequest", response=str(ex))

    def update(self, user, body):
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize(body)
        user_record.update_user()

        if hasattr(body, "complete_register"):
            user_record.make_claims({"complete_register": body["complete_register"]})

        _user.serialize(body)
        _user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def update_field(self, user, body):
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize(body)
        user_record.update_user()

        if hasattr(body, "complete_register"):
            user_record.make_claims({"complete_register": body["complete_register"]})

        _user.serialize(body)
        _user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def disabled(self, user):
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.serialize({"disabled": not user_record.disabled})
        user_record.update_user()

        user.serialize({"disabled": not user_record.disabled})
        user.save()

        return {"uid": user_record.uid, "a": user_record, "b": _user}

    def delete(self, user):
        user_record = user["a"]
        _user = user["b"]

        if not user_record or not _user:
            abort(404, description="NotFound", response="not_found")

        user_record.delete_user()
        _user.delete()

        return {"uid": user_record.uid}
