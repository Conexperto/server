""" tests.test_speciality """
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
                "id": {"type": "number"},
                "name": {"type": "string"},
                "disabled": {"type": "boolean"},
            },
        },
    },
    "required": ["success", "response"],
}

schema_many = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {"type": "array", "items": schema["properties"]["response"]},
    },
    "required": ["success", "response"],
}

schema_list = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {"type": "array", "items": schema["properties"]["response"]},
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
        "response": {"type": "object", "properties": {"id": {"type": "number"}}},
    },
    "required": ["success", "response"],
}

schema_delete_many = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {"type": "array", "items": {"type": "number"}},
    },
    "required": ["success", "response"],
}


def search_method(client, auth, search):
    auth.login("admin@adminconexperto.com", "token_admin")
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"search": search}
    rv = client.get("/admin/method", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    return body["response"]


def prove_order(items, order):
    identifiers = [item["id"] for item in items]
    if identifiers == sorted(identifiers):
        return order == "asc"
    else:
        return order == "desc"
    return False


def paginate(client, auth, params):
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/method", query_string=params, headers=headers)
    return rv


def test_create_method(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: POST
    Assert: status_code = 200
    Description:
        Test create method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Snapchat"}
    rv = client.post("/admin/method", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_create_many_method(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: POST
    Assert: status_code = 200
    Description:
        Test create method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = [{"name": "Duo"}, {"name": "Meet"}]
    rv = client.post("/admin/method", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_many)


def test_create_method_duplicate(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: POST
    Assert: status_code = 400
    Description:
        Test create method duplicate
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Snapchat"}
    rv = client.post("/admin/method", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_create_method_without_field(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: POST
    Assert: status_code = 400
    Description:
        Test create method without field
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {}
    rv = client.post("/admin/method", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_create_method_without_headers(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: POST
    Assert: status_code = 400
    Description:
        Test create method without headers
    """
    payload = {"name": "Snapchat"}
    rv = client.post("/admin/method", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_update_method(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/<id>
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Method"}
    method = search_method(client, auth, "Snapchat")
    rv = client.put(
        "/admin/method/" + str(method[0]["id"]), headers=headers, json=payload
    )
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)

    assert (
        body["response"]["name"] == payload["name"]
    ), "should be equal to payload name"


def test_update_method_field(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/<id>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test update method field
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Snapchat"}
    method = search_method(client, auth, "Method")
    rv = client.patch(
        "/admin/method/" + str(method[0]["id"]), headers=headers, json=payload
    )
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)

    assert (
        body["response"]["name"] == payload["name"]
    ), "should be equal to payload name"


def test_update_many_method(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update many method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    method = search_method(client, auth, "")
    payload = [
        {"id": method[0]["id"], "name": "Meet You"},
        {"id": method[1]["id"], "name": "Room Only"},
    ]
    rv = client.put("/admin/method", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_many)

    for i in range(2):
        assert (
            body["response"][i]["name"] == payload[i]["name"]
        ), "should be equal to payload"


def test_get_method(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/<id>
    Method: GET
    Assert: status_code = 200
    Description:
        Test get by method id
    """
    headers = {"Authorization": "Bearer " + auth.token}
    method = search_method(client, auth, "Duo")
    rv = client.get("/admin/method/" + str(method[0]["id"]), headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_list_method(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/method", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_method_search(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: GET
    Assert: status_code = 200
    Description:
        Test search method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {
        "search": "Skype",
    }
    rv = client.get("/admin/method", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_method_paginate(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method pagination
    """
    params = {"page": 1, "limit": 2}
    while True:
        rv = paginate(client, auth, params)
        assert rv.status_code == 200, "should be status code 200"
        assert (
            rv.headers["Content-Type"] == "application/json"
        ), "should be content type application/json"
        body = loads(rv.data)
        assert body["page"] == params["page"], "should be equal to params page"
        validate(instance=body, schema=schema_list)
        params["page"] = body["next"]
        if not body["next"]:
            return


def test_list_method_desc(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method with order desc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/admin/method", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "desc"), "should be sorted in descending order"


def test_list_method_asc(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method with order asc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/admin/method", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "desc"), "should be sorted in descending order"


def test_method_disabled(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/disabled/<id>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test disabled method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    method = search_method(client, auth, "Duo")
    rv = client.patch("/admin/method/disabled/" + str(method[0]["id"]), headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
    assert body["response"]["disabled"] is True, "should be disabled True"


def test_list_method_disabled(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method?disabled=true
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method filter by disabled true
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/method", query_string={"disabled": True}, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)

    for item in body["response"]:
        assert item["disabled"] is True, "should be disabled True"


def test_method_enabled(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/disabled/<id>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test enabled method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    method = search_method(client, auth, "Duo")
    rv = client.patch("/admin/method/disabled/" + str(method[0]["id"]), headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)

    assert body["response"]["disabled"] is False, "should be disabled False"


def test_method_disabled_many(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/disabled
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test disabled many specialities
    """
    headers = {"Authorization": "Bearer " + auth.token}

    methods = search_method(client, auth, "")
    payload = [item["id"] for item in methods[3:5]]

    rv = client.patch("/admin/method/disabled", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_many)

    for i in range(2):
        assert body["response"][i]["disabled"] is True, "should be disabled True"


def test_method_enabled_many(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/disabled
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test enabled many methods
    """
    headers = {"Authorization": "Bearer " + auth.token}

    methods = search_method(client, auth, "")
    payload = [item["id"] for item in methods[3:5]]

    rv = client.patch("/admin/method/disabled", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_many)

    for i in range(2):
        assert body["response"][i]["disabled"] is False, "should be disabled False"


def test_method_delete(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method/<id>
    Method: DELETE
    Assert: status_code = 200
    Description:
        Test delete method
    """
    headers = {"Authorization": "Bearer " + auth.token}
    method = search_method(client, auth, "Duo")
    rv = client.delete("/admin/method/" + str(method[0]["id"]), headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_delete)


def test_method_delete_many(client, auth, login_admin, seed_method):
    """
    Endpoint: /admin/method
    Method: DELETE
    Assert: status_code = 200
    Description:
        Test delete many method
    """
    headers = {"Authorization": "Bearer " + auth.token}

    methods = search_method(client, auth, "")
    payload = [item["id"] for item in methods[3:5]]

    rv = client.delete("/admin/method", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_delete_many)
