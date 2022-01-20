""" tests.test_auth_admin """
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
                        "photo_url": {
                            "oneOf": [{"type": "string"}, {"type": "null"}]
                        },
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
                        "privileges": {"type": "number"},
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


def test_auth_user(client, auth, login_user):
    """
    Endpoint: /admin/auth
    Method: GET
    Assert: status_code == 200
    Description:
        Test admin auth
    """
    rv = client.get(
        "/admin/auth", headers={"Authorization": "Bearer " + auth.token}
    )
    assert rv.status_code == 200, "should be status code 200"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_without_headers(client):
    """
    Endpoint: /admin/auth
    Method: GET
    Assert: status_code == 400
    Description:
        Test admin auth without headers
    """
    rv = client.get("/admin/auth")
    assert rv.status_code == 400, "should be status code 400"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_wrong_token(client):
    """
    Endpoint: /admin/auth
    Method: GET
    Assert: status_code == 400
    Description:
        Test admin auth without token
    """
    rv = client.get("/admin/auth", headers={"Authorization": "Bearer"})
    assert rv.status_code == 400, "should be status code 400"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_update(client, auth, login_user):
    """
    Endpoint: /admin/auth
    Method: PUT
    Assert: status_code == 200
    Description:
        Test update user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+10000000001",
        "name": "Testing",
        "lastname": "Testing",
    }
    rv = client.put("/admin/auth", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_disabled(client, auth, login_user):
    """
    Endpoint: /admin/auth
    Method: PATCH
    Assert: status_code == 200
    Description:
        Test disabled user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.patch("/admin/auth/disabled", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
