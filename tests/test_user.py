""" tests.test_user """
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

schema_delete = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "response": {
            "type": "object",
            "properties": {"uid": {"type": "string"}},
        },
    },
}


def search_user(client, search):
    params = {"search": search}
    rv = client.get("/users", query_string=params)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    logger.info(body)
    return body["response"]


def prove_order(items, order):
    identifiers = [item["id"] for item in items]
    if identifiers == sorted(identifiers):
        return order == "asc"
    else:
        return order == "desc"
    return False


def paginate(client, params):
    rv = client.get("/users", query_string=params)
    return rv


def test_get_user(client, auth):
    """
    Endpoint: /users/<uid>
    Method: GET
    Assert: status_code = 200
    Description:
        Test get by user uid
    """
    user = search_user(client, "user@conexperto.com")
    rv = client.get("/users/" + user[0]["uid"])
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_list_user(client, auth):
    """
    Endpoint: /users
    Method: GET
    Assert: status_code = 200
    Description:
        Test list user
    """
    rv = client.get("/users")
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_user_search(client, auth):
    """
    Endpoint: /users
    Method: GET
    Assert: status_code = 200
    Description:
        Test search user
    """
    params = {
        "search": "Startups",
    }
    rv = client.get("/users", query_string=params)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_user_paginate(client, auth):
    """
    Endpoint: /users
    Method: GET
    Assert: status_code = 200
    Description:
        Test list user pagination
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


def test_list_user_order_asc(client, auth):
    """
    Endpoint: /users
    Method: GET
    Assert: status_code = 200
    Description:
        Test list user with order asc
    """
    params = {"orderBy": "id", "order": "asc"}
    rv = client.get("/users", query_string=params)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(
        body["response"], "asc"
    ), "should be sorted in ascending order"


def test_list_user_order_desc(client, auth):
    """
    Endpoint: /users
    Method: GET
    Assert: status_code = 200
    Description:
        Test list user with order desc
    """
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/users", query_string=params)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(
        body["response"], "desc"
    ), "should be sorted in descending order"
