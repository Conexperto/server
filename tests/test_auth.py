""" tests.test_auth """
import logging
from json import loads

from faker import Faker
from jsonschema import validate


faker = Faker()
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
                        "rating_average": {"type": "number"},
                        "rating_stars": {
                            "type": "array",
                            "items": {
                                "type": "number",
                                "minItems": 5,
                                "maxItems": 5,
                            },
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


def get_user(client, auth):
    auth.login("test@conexperto.com", "token_test")
    rv = client.get("/auth", headers={"Authorization": "Bearer " + auth.token})
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
    return body


def get_speciality(client):
    rv = client.get("/specialities")
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    return body["response"]


def get_method(client):
    rv = client.get("/methods")
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    return body["response"]


def test_auth_create(client, auth):
    """
    Endpoint: /auth
    Method: POST
    Assert: status_code == 200
    Description:
        Test create user
    """
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
    """
    Endpoint: /auth
    Method: POST
    Assert: status_code == 200
    Description:
        Test create user
    """
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
    """
    Endpoint: /auth
    Method: POST
    Assert: status_code == 400
    Description:
        Test create user without field
    """
    payload = {
        "email": "test@conexperto.com",
    }
    rv = client.post("/auth", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth(client, auth):
    """
    Endpoint: /auth
    Method: GET
    Assert: status_code == 200
    Description:
        Test get user authenticated
    """
    auth.login("test@conexperto.com", "token_test")
    rv = client.get("/auth", headers={"Authorization": "Bearer " + auth.token})
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_without_headers(client):
    """
    Endpoint: /auth
    Method: GET
    Assert: status_code == 400
    Description:
        Test get user authenticated without headers
    """
    rv = client.get("/auth")
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_wrong_token(client):
    """
    Endpoint: /auth
    Method: GET
    Assert: status_code == 400
    Description:
        Test get user authenticated with wring token
    """
    rv = client.get("/auth", headers={"Authorization": "Bearer"})
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_create_extra_field(client):
    """
    Endpoint: /auth
    Method: POST
    Assert: status_code == 400
    Description:
        Test get user authenticated with extra field
    """
    payload = {"email": "test@conexperto.com", "passport": "ABC1235598A"}
    rv = client.post("/auth", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_update(client, auth, seed_speciality, seed_method):
    """
    Endpoint: /auth
    Method: PUT
    Assert: status_code == 200
    Description:
        Test update user authenticated
    """
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+11000010000",
        "name": "Testing",
        "lastname": "Testing",
        "headline": "Lorem ipsum",
        "about_me": "Lorem ipsum",
        "link_video": "https://www.youtube.com",
        "location": faker.country(),
        "timezone": "GMT",
        "specialities": [item["id"] for item in get_speciality(client)[:3]],
        "methods": [
            {"id": item["id"], "link": faker.url()}
            for item in get_method(client)[:3]
        ],
        "plans": [{"duration": 60, "price": 15}],
    }
    rv = client.put("/auth", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_update_specialities(client, auth, seed_speciality):
    """
    Endpoint: /api/v1/auth/specialities
    Method: PUT
    Assert: status_code 200
    Description:
        Test update user specialities authenticated
    """
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = [item["id"] for item in get_speciality(client)[:6]]
    rv = client.put("/auth/specialities", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_update_methods(client, auth, seed_method):
    """
    Endpoint: /api/v1/auth/specialities
    Method: PUT
    Assert: status_code 200
    Description:
        Test update user methods authenticated
    """
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = [
        {"link": faker.url(), "id": item["id"]}
        for item in get_method(client)[:6]
    ]
    rv = client.put("/auth/methods", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_update_plans(client, auth):
    """
    Endpoint: /api/v1/auth/plans
    Method: PUT
    Assert: status_code 200
    Description:
        Test update user plans authenticated
    """
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = [
        *get_user(client, auth)["response"]["b"]["plans"],
        {"duration": 120, "price": 12},
    ]
    rv = client.put("/auth/plans", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_update_duplicate_phone_number(client, auth):
    """
    Endpoint: /auth
    Method: PUT
    Assert: status_code == 400
    Description:
        Test update user authenticated with duplicate phone number
    """
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
    assert rv.status_code == 400, "should be status code 400"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_update_field(client, auth):
    """
    Endpoint: /auth
    Method: PATCH
    Assert: status_code == 200
    Description:
        Test update filed user authenticated
    """
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"display_name": "testing"}
    rv = client.patch("/auth", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_auth_update_field_duplicate_phone_number(client, auth):
    """
    Endpoint: /auth
    Method: PATCH
    Assert: status_code == 200
    Description:
        Test update filed user authenticated with duplicate phone number
    """
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"phone_number": "+10000000000"}
    rv = client.patch("/auth", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_auth_disabled(client, auth):
    """
    Endpoint: /auth/disabled
    Method: PATCH
    Assert: status_code == 200
    Description:
        Test disabled user authenticated
    """
    auth.login("test@conexperto.com", "token_test")
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.patch("/auth/disabled", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert rv.headers["Content-Type"] == "application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
