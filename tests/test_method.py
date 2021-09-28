""" tests.test_method """
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


def search_method(client, search):
    params = {"search": search}
    rv = client.get("/method", query_string=params)
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


def paginate(client, params):
    rv = client.get("/method", query_string=params)
    return rv


def test_get_method(client, seed_method):
    """
    Endpoint: /method/<id>
    Method: GET
    Assert: status_code = 200
    Description:
        Test get by method id
    """
    method = search_method(client, "Skype")
    rv = client.get("/method/" + str(method[0]["id"]))
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_list_method(client, seed_method):
    """
    Endpoint: /method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method
    """
    rv = client.get("/method")
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_method_search(client, seed_method):
    """
    Endpoint: /method
    Method: GET
    Assert: status_code = 200
    Description:
        Test search method
    """
    params = {
        "search": "Skype",
    }
    rv = client.get("/method", query_string=params)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_method_paginate(client, seed_method):
    """
    Endpoint: /method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method pagination
    """
    params = {"page": 1, "limit": 2}
    while True:
        rv = paginate(client, params)
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


def test_list_method_desc(client, seed_method):
    """
    Endpoint: /method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method with order desc
    """
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/method", query_string=params)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(
        body["response"], "desc"
    ), "should be sorted in descending order"


def test_list_method_asc(client, seed_method):
    """
    Endpoint: /method
    Method: GET
    Assert: status_code = 200
    Description:
        Test list method with order asc
    """
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/method", query_string=params)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(
        body["response"], "desc"
    ), "should be sorted in descending order"
