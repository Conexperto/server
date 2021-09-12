""" tests.test_auth """
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
                "uid": {"type": "string"},
                "a": {
                    "type": "object",
                    "properties": {
                        "uid": {"type": "string"},
                        "email": {"type": "string"},
                        "email_verified": {"type": "boolean"},
                        "display_name": {"type": "string"},
                        "phone_number": {
                            "oneOf": [{"type": "string"}, {"type": "null"}]
                        },
                        "photo_url": {"oneOf": [{"type": "string"}, {"type": "null"}]},
                        "disabled": {"type": "boolean"},
                        "provider_data": {
                            "type": "array",
                            "items": {
                                "uid": {"type": "string"},
                                "display_name": {"type": "string"},
                                "email": {"type": "string"},
                                "phone_number": {"type": "string"},
                                "photo_url": {"type": "string"},
                                "provider_id": {"type": "string"},
                            },
                        },
                        "custom_claims": {"type": ["object", "null"]},
                    },
                },
                "b": {
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
                        "rating_stars": {
                            "type": "array",
                            "items": {"type": "number", "minItems": 5, "maxItems": 5},
                        },
                        "rating_votes": {"type": "number"},
                        "headline": {"type": ["string", "null"]},
                        "about_me": {"type": ["string", "null"]},
                        "session_taken": {"type": "number"},
                        "complete_register": {"type": "boolean"},
                        "timezone": {"type": ["string", "null"]},
                        "link_video": {"type": ["string", "null"]},
                        "location": {"type": ["string", "null"]},
                        "plans": {
                            "type": "array",
                            "items": {
                                "id": {"type": "number"},
                                "duration": {"type": "number"},
                                "price": {"type": "number"},
                                "coin": {"type": "string"},
                                "disabled": {"type": "boolean"},
                                "user_id": {"type": "number"},
                            },
                        },
                        "specialities": {
                            "type": "array",
                            "items": {
                                "left_id": {"type": "number"},
                                "right_id": {"type": "number"},
                                "disabled": {"type": "booelan"},
                                "speciality": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "number"},
                                        "name": {"type": "string"},
                                        "disabled": {"type": "boolean"},
                                    },
                                },
                            },
                        },
                        "methods": {
                            "type": "array",
                            "items": {
                                "left_id": {"type": "number"},
                                "right_id": {"type": "number"},
                                "link": {"type": "string"},
                                "disabled": {"type": "booelan"},
                                "method": {
                                    "type": "object",
                                    "properties": {
                                        "id": {"type": "number"},
                                        "name": {"type": "string"},
                                        "disabled": {"type": "boolean"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
            "required": ["uid", "a", "b"],
        },
    },
    "required": ["success", "response"],
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


def test_auth_create(client):
    payload = {
        "email": "test@conexperto.com",
        "password": "token_test",
        "display_name": "Testing",
    }
    rv = client.post("/auth", json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_create_duplicate(client, auth):
    payload = {
        "email": "test@conexperto.com",
        "password": "token_test",
        "display_name": "Testing",
    }
    rv = client.post("/auth", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_create_without_field(client):
    payload = {
        "email": "test@conexperto.com",
    }
    rv = client.post("/auth", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth(client, auth):
    auth.login("test@conexperto.com", "token_test")
    rv = client.get("/auth", headers={"Authorization": "Bearer " + auth.token})
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_wrong_user(client, auth, login_user):
    rv = client.get("/auth", headers={"Authorization": "Bearer " + auth.token})
    assert rv.status_code == 404, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_without_headers(client):
    rv = client.get("/auth")
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_wrong_token(client):
    rv = client.get("/auth", headers={"Authorization": "Bearer"})
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_create_extra_field(client):
    payload = {"email": "test@conexperto.com", "passport": "ABC1235598A"}
    rv = client.post("/auth", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_update(client, auth):
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+11000010000",
        "name": "Testing",
        "lastname": "Testing",
        "headline": "Lorem ipsum",
        "about_me": "Lorem ipsum",
    }
    rv = client.put("/auth", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_update_duplicate_phone_number(client, auth):
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+10000000000",
        "name": "Testing",
        "lastname": "Testing",
        "headline": "Lorem ipsum",
        "about_me": "Lorem ipsum",
    }
    rv = client.put("/auth", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_update_field(client, auth):
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"display_name": "testing"}
    rv = client.patch("/auth", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_update_field_duplicate_phone_number(client, auth):
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"phone_number": "+10000000000"}
    rv = client.patch("/auth", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_disabled(client, auth):
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.patch("/auth/disabled", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
