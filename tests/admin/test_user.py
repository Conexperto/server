""" tests.test_user_admin """
import logging
from json import loads

from jsonschema import validate


logger = logging.getLogger(__name__)


schema = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {
            "type": "object",
            "properties": {
                "id": {"type": "number"},
                "uid": {"type": "string"},
                "display_name": {"type": "string"},
                "email": {"type": "string"},
                "phone_number": {"type": ["string", "null"]},
                "photo_url": {"type": ["string", "null"]},
                "name": {"type": ["string", "null"]},
                "lastname": {"type": ["string", "null"]},
                "disabled": {"type": "boolean"},
                "rating_average": {"type": "number"},
                "rating_stars": {"type": "array", "items": {"type": "number"}},
                "rating_votes": {"types": "number"},
                "headline": {"type": "string"},
                "about_me": {"type": "string"},
                "session_taken": {"type": "number"},
                "complete_register": {"type": "boolean"},
                "timezone": {"type": "string"},
                "link_video": {"type": "string"},
                "location": {"type": "string"},
                "plans": {
                    "type": "array",
                    "items": {
                        "id": {"type": "number"},
                        "duration": {"type": "number"},
                        "price": {"type": "number"},
                        "coin": {"type": "string"},
                    },
                },
                "specialities": {
                    "type": "array",
                    "items": {
                        "id": {"type": "string"},
                        "left_id": {"type": "number"},
                        "right_id": {"type": "number"},
                        "speciality": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "number"},
                                "name": {"type": "string"},
                            },
                        },
                    },
                },
                "methods": {
                    "type": "array",
                    "items": {
                        "id": {"type": "string"},
                        "left_id": {"type": "number"},
                        "right_id": {"type": "number"},
                        "methods": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "number"},
                                "name": {"type": "string"},
                            },
                        },
                        "link": {"type": "string"},
                    },
                },
            },
            "required": ["uid"],
        },
    },
    "required": ["success", "response"],
}

schema_list = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {
            "type": "array",
            "items": schema["properties"]["response"],
        },
        "total": {"type": "number"},
        "page": {"type": "number"},
        "limit": {"type": "number"},
        "next": {"type": ["number", "null"]},
    },
    "required": ["success", "response", "total", "page", "limit", "next"],
}

schema_error = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "err": {"type": "number"},
        "msg": {"type": "string"},
    },
    "required": ["success", "err", "msg"],
}


def search_user(client, auth, search):
    auth.login("admin@adminconexperto.com", "token_admin")
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"search": search}
    rv = client.get("/admin/user", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    return body["response"][0]["uid"]


def prove_order(items, order):
    identifiers = [item["id"] for item in items]
    if identifiers == sorted(identifiers):
        return order == "asc"
    else:
        return order == "desc"
    return False


def paginate(client, auth, params):
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin", query_string=params, headers=headers)
    return rv


# def test_create_user(client, auth, login_admin):
#    headers = {"Authorization": "Bearer " + auth.token}
#    payload = {
#        "email": "test@adminconexperto.com",
#        "password": "token_test",
#        "display_name": "Testing",
#        "phone_number": "+13100000000",
#        "name": "Testing",
#        "lastname": "Testing",
#    }
