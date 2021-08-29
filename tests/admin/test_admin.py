""" tests.admin.test_admin """
import logging
from json import dumps
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
        "detail": {"type": "string"},
        "code": {"type": "string"},
    },
    "required": ["success", "err", "msg", "detail", "code"],
}


def test_admin_create_user(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test@adminconexperto.com",
        "password": "token_test",
        "display_name": "Testing",
        "phone_number": "+13100000000",
        "name": "Testing",
        "lastname": "Testing",
        "privileges": 3,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_create_user_duplicate(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test@adminconexperto.com",
        "password": "token_test",
        "display_name": "Testing",
        "phone_number": "+13100000000",
        "name": "Testing",
        "lastname": "Testing",
        "privileges": 3,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_create_user_without_field(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test@adminconexperto.com",
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_create_admin(client, auth, login_root):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test_admin@adminconexperto.com",
        "password": "token_admin",
        "display_name": "Testing Admin",
        "phone_number": "+13200000000",
        "name": "Testing Admin",
        "lastname": "Testing",
        "privileges": 2,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_create_admin_without_headers(client):
    payload = {
        "email": "test_admin@adminconexperto.com",
        "password": "token_admin",
        "display_name": "Testing Admin",
        "phone_number": "+13200000000",
        "name": "Testing Admin",
        "lastname": "Testing",
        "privileges": 1,
    }
    rv = client.post("/admin", json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_create_admin_wrong_token(client):
    headers = {"Authorization": "Bearer "}
    payload = {
        "email": "test_admin@adminconexperto.com",
        "password": "token_admin",
        "display_name": "Testing Admin",
        "phone_number": "+13200000000",
        "name": "Testing Admin",
        "lastname": "Testing",
        "privileges": 1,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_create_root(client, auth, login_superroot):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test_root@adminconexperto.com",
        "password": "token_root",
        "display_name": "Testing Root",
        "phone_number": "+13300000000",
        "name": "Testing Root",
        "lastname": "Testing",
        "privileges": 1,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_create_root_wrong_auth(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test_admin@adminconexperto.com",
        "password": "token_admin",
        "display_name": "Testing Admin",
        "phone_number": "+13200000000",
        "name": "Testing Admin",
        "lastname": "Testing",
        "privileges": 1,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 401, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_create_superroot(client, auth, login_superroot):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test_superroot@adminconexperto.com",
        "password": "token_superroot",
        "display_name": "Testing SuperRoot",
        "phone_number": "+13400000000",
        "name": "Testing SuperRoot",
        "lastname": "Testing",
        "privileges": 0,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_create_superroot_wrong_auth(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test_admin@adminconexperto.com",
        "password": "token_admin",
        "display_name": "Testing Admin",
        "phone_number": "+13200000000",
        "name": "Testing Admin",
        "lastname": "Testing",
        "privileges": 0,
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 401, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_update_user(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "display_name": "Testing SuperRoot SuperRoot",
        "name": "Testing SuperRoot SuperRoot",
        "lastname": "Testing SuperRoot",
    }
    rv = client.put("/admin/" + auth.user["localId"], headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_update_user_duplicate_phone_number(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+13100000000",
        "name": "Testing SuperRoot",
        "lastname": "Testing SuperRoot",
    }
    rv = client.put("/admin/" + auth.user["localId"], headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_update_field(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "display_name": "Testing SuperRoot",
    }
    rv = client.patch("/admin/" + auth.user["localId"], headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_update_field_duplicate_phone_number(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+13100000000",
    }
    rv = client.patch("/admin/" + auth.user["localId"], headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_get_user(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/" + auth.user["localId"], headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_get_user_wrong_auth(client, auth, login_user):
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/" + auth.user["localId"], headers=headers)
    assert rv.status_code == 401, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_list_user(client, auth, login_admin):
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    logger.info(dumps(body, indent=2))
    # validate(instance=body, schema=schema)
