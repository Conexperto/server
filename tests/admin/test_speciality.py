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


def search_speciality(client, auth, search):
    auth.login("admin@adminconexperto.com", "token_admin")
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"search": search}
    rv = client.get("/admin/speciality", query_string=params, headers=headers)
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
    rv = client.get("/admin/speciality", query_string=params, headers=headers)
    return rv


def test_create_speciality(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: POST
    Assert: status_code = 200
    Description:
        Test create speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Teacher"}
    rv = client.post("/admin/speciality", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_create_many_speciality(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: POST
    Assert: status_code = 200
    Description:
        Test create speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = [{"name": "Astronomer"}, {"name": "Physicist"}]
    rv = client.post("/admin/speciality", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_many)


def test_create_speciality_duplicate(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: POST
    Assert: status_code = 400
    Description:
        Test create speciality duplicate
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Teacher"}
    rv = client.post("/admin/speciality", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_create_speciality_without_field(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: POST
    Assert: status_code = 400
    Description:
        Test create speciality without field
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {}
    rv = client.post("/admin/speciality", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_create_speciality_without_headers(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: POST
    Assert: status_code = 400
    Description:
        Test create speciality without headers
    """
    payload = {"name": "Teacher"}
    rv = client.post("/admin/speciality", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_update_speciality(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/<id>
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Speciality"}
    speciality = search_speciality(client, auth, "Teacher")
    rv = client.put(
        "/admin/speciality/" + str(speciality[0]["id"]), headers=headers, json=payload
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


def test_update_speciality_field(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/<id>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test update speciality field
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {"name": "Teacher"}
    speciality = search_speciality(client, auth, "Speciality")
    rv = client.patch(
        "/admin/speciality/" + str(speciality[0]["id"]), headers=headers, json=payload
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


def test_update_many_speciality(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update many speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    speciality = search_speciality(client, auth, "")
    payload = [
        {"id": speciality[0]["id"], "name": "Police"},
        {"id": speciality[1]["id"], "name": "Medic"},
    ]
    rv = client.put("/admin/speciality", headers=headers, json=payload)
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


def test_get_speciality(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/<id>
    Method: GET
    Assert: status_code = 200
    Description:
        Test get by speciality id
    """
    headers = {"Authorization": "Bearer " + auth.token}
    speciality = search_speciality(client, auth, "Medic")
    rv = client.get("/admin/speciality/" + str(speciality[0]["id"]), headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_list_speciality(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: GET
    Assert: status_code = 200
    Description:
        Test list speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/speciality", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_speciality_search(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: GET
    Assert: status_code = 200
    Description:
        Test search speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {
        "search": "Medic",
    }
    rv = client.get("/admin/speciality", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_speciality_paginate(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: GET
    Assert: status_code = 200
    Description:
        Test list speciality pagination
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
        assert body["page"] == params["page"], "should be equal to params page"
        validate(instance=body, schema=schema_list)
        params["page"] = body["next"]
        if not body["next"]:
            return


def test_list_speciality_desc(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: GET
    Assert: status_code = 200
    Description:
        Test list speciality with order desc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/admin/speciality", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "desc"), "should be sorted in descending order"


def test_list_speciality_asc(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: GET
    Assert: status_code = 200
    Description:
        Test list speciality with order asc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/admin/speciality", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "desc"), "should be sorted in descending order"


def test_speciality_disabled(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/disabled/<id>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test disabled speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    speciality = search_speciality(client, auth, "Medic")
    rv = client.patch(
        "/admin/speciality/disabled/" + str(speciality[0]["id"]), headers=headers
    )
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
    assert body["response"]["disabled"] is True, "should be disabled True"


def test_speciality_enabled(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/disabled/<id>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test enabled speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    speciality = search_speciality(client, auth, "Medic")
    rv = client.patch(
        "/admin/speciality/disabled/" + str(speciality[0]["id"]), headers=headers
    )
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)

    assert body["response"]["disabled"] is False, "should be disabled False"


def test_speciality_disabled_many(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/disabled
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test disabled many specialities
    """
    headers = {"Authorization": "Bearer " + auth.token}

    specialities = search_speciality(client, auth, "")
    payload = [item["id"] for item in specialities[3:5]]

    rv = client.patch("/admin/speciality/disabled", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_many)

    for i in range(2):
        assert body["response"][i]["disabled"] is True, "should be disabled True"


def test_speciality_enabled_many(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/disabled
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test enabled many specialities
    """
    headers = {"Authorization": "Bearer " + auth.token}

    specialities = search_speciality(client, auth, "")
    payload = [item["id"] for item in specialities[3:5]]

    rv = client.patch("/admin/speciality/disabled", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_many)

    for i in range(2):
        assert body["response"][i]["disabled"] is False, "should be disabled False"


def test_speciality_delete(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality/<id>
    Method: DELETE
    Assert: status_code = 200
    Description:
        Test delete speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}
    speciality = search_speciality(client, auth, "Medic")
    rv = client.delete("/admin/speciality/" + str(speciality[0]["id"]), headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_delete)


def test_speciality_delete_many(client, auth, login_admin, seed_speciality):
    """
    Endpoint: /admin/speciality
    Method: DELETE
    Assert: status_code = 200
    Description:
        Test delete many speciality
    """
    headers = {"Authorization": "Bearer " + auth.token}

    specialities = search_speciality(client, auth, "")
    payload = [item["id"] for item in specialities[3:5]]

    rv = client.delete("/admin/speciality", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_delete_many)
