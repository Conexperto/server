""" tests.admin.test_admin """
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
                        "phone_number": {"type": ["string", "null"]},
                        "photo_url": {"type": ["string", "null"]},
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

schema_list = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {
            "type": "array",
            "items": {
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

schema_delete = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {"type": "object", "properties": {"uid": {"type": "string"}}},
    },
}


def search_user(client, auth, search):
    auth.login("admin@adminconexperto.com", "token_admin")
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"search": search}
    rv = client.get("/admin", query_string=params, headers=headers)
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


def test_admin_create_user(client, auth, login_admin):
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 200
    Description:
        Test create admin
    """
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
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 400
    Description:
        Test create admin duplicate
    """
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
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_create_user_without_field(client, auth, login_admin):
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 400
    Description:
        Test create admin without field
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "test@adminconexperto.com",
    }
    rv = client.post("/admin", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 300"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_create_admin(client, auth, login_root):
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 200
    Description:
        Test create admin
    """
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
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 400
    Description:
        Test create admin without headers
    """
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
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 401
    Description:
        Test create admin with wrong token
    """
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
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 200
    Description:
        Test create root
    """
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
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 401
    Description:
        Test create root with wrong auth
    """
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
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 200
    Description:
        Test create superroot
    """
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
    """
    Endpoint: /admin
    Method: POST
    Assert: status_code = 401
    Description:
        Test create superroot with wrong auth
    """
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
    """
    Endpoint: /admin/<uid>
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "display_name": "Testing SuperRoot SuperRoot",
        "name": "Testing SuperRoot SuperRoot",
        "lastname": "Testing SuperRoot",
    }
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.put("/admin/" + identifier, headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_update_user_duplicate_phone_number(client, auth, login_admin):
    """
    Endpoint: /admin/<uid>
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update admin with duplicate phone number
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+13200000000",
    }
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.put("/admin/" + identifier, headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_update_field(client, auth, login_admin):
    """
    Endpoint: /admin/<uid>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test update field of admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "display_name": "Testing SuperRoot",
    }
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.patch("/admin/" + identifier, headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_update_field_duplicate_phone_number(client, auth, login_admin):
    """
    Endpoint: /admin/<uid>
    Method: PATCH
    Assert: status_code = 400
    Description:
        Test update field of admin with duplicate phone number
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "phone_number": "+13200000000",
    }
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.patch("/admin/" + identifier, headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_get_user(client, auth, login_admin):
    """
    Endpoint: /admin/<uid>
    Method: GET
    Assert: status_code = 200
    Description:
        Test get by uid admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/" + auth.user["localId"], headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_admin_get_user_wrong_auth(client, auth, login_user):
    """
    Endpoint: /admin/<uid>
    Method: GET
    Assert: status_code = 401
    Description:
        Test get by uid admin with wrong auth
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/" + auth.user["localId"], headers=headers)
    assert rv.status_code == 401, "should be status code 401"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_list_user(client, auth, login_admin):
    """
    Endpoint: /admin
    Method: GET
    Assert: status_code = 200
    Description:
        Test list admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_admin_list_user_search(client, auth, login_admin):
    """
    Endpoint: /admin
    Method: GET
    Assert: status_code = 200
    Description:
        Test search admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {
        "search": "test_admin@admin",
    }
    rv = client.get("/admin", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_admin_list_user_paginate(client, auth, login_admin):
    """
    Endpoint: /admin
    Method: GET
    Assert: status_code = 200
    Description:
        Test list admin pagination
    """
    params = {"page": 1, "limit": 2}
    while True:
        rv = paginate(client, auth, params)
        assert rv.status_code == 200, "should be status code 200"
        assert (
            rv.headers["Content-Type"] == "application/json"
        ), "should be content type application/json"
        body = loads(rv.data)
        assert len(body["response"]) == 2, "should be length 2 items"
        assert body["page"] == params["page"], "should be page 2"
        validate(instance=body, schema=schema_list)
        params["page"] = body["next"]
        if not body["next"]:
            return


def test_admin_list_user_order_asc(client, auth, login_admin):
    """
    Endpoint: /admin
    Method: GET
    Assert: status_code = 200
    Description:
        Test list admin with order asc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "asc"}
    rv = client.get("/admin", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "asc"), "should be sorted in ascending order"


def test_admin_list_user_order_desc(client, auth, login_admin):
    """
    Endpoint: /admin
    Method: GET
    Assert: status_code = 200
    Description:
        Test list admin with order desc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/admin", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "desc"), "should be sorted in descending order"


def test_admin_disabled(client, auth, login_admin):
    """
    Endpoint: /admin/disabled/<uid>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test disabled admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.patch("/admin/disabled/" + identifier, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
    assert body["response"]["a"]["disabled"] is True, "should be disabled True"
    assert body["response"]["b"]["disabled"] is True, "should be disabled True"


def test_admin_enabled(client, auth, login_admin):
    """
    Endpoint: /admin/disabled/<uid>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test enabled admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.patch("/admin/disabled/" + identifier, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
    assert body["response"]["a"]["disabled"] is False, "should be disabled False"
    assert body["response"]["b"]["disabled"] is False, "should be disabled False"


def test_admin_disabled_wrong_auth(client, auth, login_user):
    """
    Endpoint: /admin/disabled/<uid>
    Method: PATCH
    Assert: status_code = 401
    Description:
        Test disabled admin with wrong auth
    """
    headers = {"Authorization": "Bearer " + auth.token}
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.patch("/admin/disabled/" + identifier, headers=headers)
    assert rv.status_code == 401, "should be status code 401"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_disabled_user_root_wrong_auth(client, auth, login_admin):
    """
    Endpoint: /admin/disabled
    Method: PATCH
    Assert: status_code == 401
    Description:
        Test admin disabled to user root from auth admin
    """
    headers = {"Authorization": "Bearer " + auth.token}
    identifier = search_user(client, auth, "test_root@adminconexperto.com")
    rv = client.patch("/admin/disabled/" + identifier, headers=headers)
    assert rv.status_code == 401, "should be status code 401"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_admin_delete(client, auth, login_admin):
    """
    Endpoint: /admin/<uid>
    Method: DELETE
    Assert: status_code = 200
    Description:
        Test admin delete
    """
    headers = {"Authorization": "Bearer " + auth.token}
    identifier = search_user(client, auth, "test@adminconexperto.com")
    rv = client.delete("/admin/" + identifier, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_delete)


def test_admin_delete_wrong_auth(client, auth, login_user):
    """
    Endpoint: /admin/<uid>
    Method: DELETE
    Assert: status_code = 200
    Description:
        Test admin delete
    """
    headers = {"Authorization": "Bearer " + auth.token}
    identifier = search_user(client, auth, "test_root@adminconexperto.com")
    rv = client.delete("/admin/" + identifier, headers=headers)
    assert rv.status_code == 401, "should be status code 401"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)
