""" tests.test_user_admin """
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
        "response": {"type": "object", "properties": {"uid": {"type": "string"}}},
    },
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
    return body["response"]


def get_speciality(client, auth):
    auth.login("admin@adminconexperto.com", "token_admin")
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/speciality", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    return body["response"]


def get_method(client, auth):
    auth.login("admin@adminconexperto.com", "token_admin")
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/method", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
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
    rv = client.get("/admin/user", query_string=params, headers=headers)
    return rv


def test_create_user(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user
    Method: POST
    Assert: status_code = 200
    Description:
        Test create user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "user@common.com",
        "password": "token_common",
        "display_name": "user_common",
        "phone_number": "+11111110000",
        "photo_url": faker.image_url(),
        "name": "user_common",
        "lastname": "",
        "headline": faker.text(max_nb_chars=50),
        "about_me": faker.text(max_nb_chars=100),
        "complete_register": True,
        "timezone": "GMT",
        "link_video": "https://youtube.com/asvasdasd",
        "location": faker.country(),
        "plans": [{"duration": 60, "price": 15}],
    }
    payload["specialities"] = [item["id"] for item in get_speciality(client, auth)[:3]]
    payload["methods"] = [
        {"id": item["id"], "link": faker.url()} for item in get_method(client, auth)[:3]
    ]
    rv = client.post("/admin/user", headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_create_user_duplicate(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user
    Method: POST
    Assert: status_code = 400
    Description:
        Test create user duplicate
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "user@common.com",
        "password": "token_common",
        "display_name": "user_common",
        "phone_number": "+11111110000",
        "photo_url": faker.image_url(),
        "name": "user_common",
        "lastname": "",
        "headline": faker.text(max_nb_chars=50),
        "about_me": faker.text(max_nb_chars=100),
        "complete_register": True,
        "timezone": "GMT",
        "link_video": "https://youtube.com/asvasdasd",
        "plans": [{"duration": 60, "price": 15}],
    }
    payload["specialities"] = [item["id"] for item in get_speciality(client, auth)]
    payload["methods"] = [
        {"id": item["id"], "link": faker.url()} for item in get_method(client, auth)
    ]
    rv = client.post("/admin/user", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_create_user_without_field(
    client, auth, login_admin, seed_speciality, seed_method
):
    """
    Endpoint: /admin/user
    Method: POST
    Assert: status_code = 400
    Description:
        Test create user without field
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "email": "user@common.com",
        "display_name": "user_common",
        "phone_number": "+11111110000",
        "photo_url": faker.image_url(),
        "name": "user_common",
        "lastname": "",
        "headline": faker.text(max_nb_chars=50),
        "about_me": faker.text(max_nb_chars=100),
        "complete_register": True,
        "timezone": "GMT",
        "link_video": "https://youtube.com/asvasdasd",
        "plans": [{"duration": 60, "price": 15}],
    }
    payload["specialities"] = [item["id"] for item in get_speciality(client, auth)]
    payload["methods"] = [
        {"id": item["id"], "link": faker.url()} for item in get_method(client, auth)
    ]
    rv = client.post("/admin/user", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_create_user_without_headers(client):
    """
    Endpoint: /admin/user
    Method: POST
    Assert: status_code = 400
    Description:
        Test create user without headers
    """
    payload = {
        "email": "user@common.com",
        "password": "token_common",
        "display_name": "user_common",
        "phone_number": "+11111110000",
        "photo_url": faker.image_url(),
        "name": "user_common",
        "lastname": "",
        "headline": faker.text(max_nb_chars=50),
        "about_me": faker.text(max_nb_chars=100),
        "complete_register": True,
        "timezone": "GMT",
        "link_video": "https://youtube.com/asvasdasd",
        "plans": [{"duration": 60, "price": 15}],
    }
    rv = client.post("/admin/user", json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_create_user_wrong_token(
    client, auth, login_admin, seed_speciality, seed_method
):
    """
    Endpoint: /admin/user
    Method: POST
    Assert: status_code = 400
    Description:
        Test create user wrong token
    """
    headers = {"Authorization": "Bearer "}
    payload = {
        "email": "user@common.com",
        "password": "token_common",
        "display_name": "user_common",
        "phone_number": "+11111110000",
        "photo_url": faker.image_url(),
        "name": "user_common",
        "lastname": "",
        "headline": faker.text(max_nb_chars=50),
        "about_me": faker.text(max_nb_chars=100),
        "complete_register": True,
        "timezone": "GMT",
        "link_video": "https://youtube.com/asvasdasd",
        "plans": [{"duration": 60, "price": 15}],
    }
    payload["specialities"] = [item["id"] for item in get_speciality(client, auth)]
    payload["methods"] = [
        {"id": item["id"], "link": faker.url()} for item in get_method(client, auth)
    ]
    rv = client.post("/admin/user", headers=headers, json=payload)
    assert rv.status_code == 400, "should be status code 400"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_error)


def test_update_user(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user/<uid>
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "display_name": "user",
        "name": "user",
        "specialities": [item["id"] for item in get_speciality(client, auth)[3:6]],
        "methods": [
            {"id": item["id"], "link": faker.url()}
            for item in get_method(client, auth)[3:6]
        ],
        "plans": [{"duration": 60, "price": 15}],
    }

    user = search_user(client, auth, "user@common.com")

    payload["methods"].append(
        {"id": user[0]["methods"][0]["right_id"], "link": faker.url()}
    )
    payload["plans"].append({"id": user[0]["plans"][0]["id"], "price": 20})

    rv = client.put("/admin/user/" + user[0]["uid"], headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)

    user_record = body["response"]["a"]
    user = body["response"]["b"]

    assert (
        user_record["display_name"] == payload["display_name"]
    ), "should be equal to payload display_name"
    assert (
        user["display_name"] == payload["display_name"]
    ), "should be equal to payload display_name"
    assert user["name"] == payload["name"], "should be equal to payload name"

    assert len(user["specialities"]) == len(
        payload["specialities"]
    ), "should be equal length to payload specialities"

    assert len(user["methods"]) == len(
        payload["methods"]
    ), "should be equal length to payload methods"

    for item in user["specialities"]:
        assert (
            item["right_id"] in payload["specialities"]
        ), "shoould be equal to payload specialities"

    for item in user["methods"]:
        assert any(
            v["id"] == item["right_id"] for v in payload["methods"]
        ), "should be equal to payload methods"
        assert any(
            v["link"] == item["link"] for v in payload["methods"]
        ), "should be equal to payload methods link"


def test_update_user_field(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user/<uid>
    Method: PUT
    Assert: status_code = 200
    Description:
        Test update user field
    """
    headers = {"Authorization": "Bearer " + auth.token}
    payload = {
        "specialities": [item["id"] for item in get_speciality(client, auth)[3:6]]
    }
    user = search_user(client, auth, "user@common.com")
    rv = client.put("/admin/user/" + user[0]["uid"], headers=headers, json=payload)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)

    user = body["response"]["b"]

    for item in user["specialities"]:
        assert (
            item["right_id"] in payload["specialities"]
        ), "shoould be equal to payload specialities"


def test_get_user(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user/<uid>
    Method: GET
    Assert: status_code = 200
    Description:
        Test get by user uid
    """
    headers = {"Authorization": "Bearer " + auth.token}
    user = search_user(client, auth, "user@common.com")
    rv = client.get("/admin/user/" + user[0]["uid"], headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)


def test_list_user(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user
    Method: GET
    Assert: status_code = 200
    Description:
        Test list user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/user", headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_user_search(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user
    Method: GET
    Assert: status_code = 200
    Description:
        Test search user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {
        "search": "Startups",
    }
    rv = client.get("/admin/user", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)


def test_list_user_paginate(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user
    Method: GET
    Assert: status_code = 200
    Description:
        Test list user pagination
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


def test_list_user_order_asc(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user
    Method: GET
    Assert: status_code = 200
    Description:
        Test list admin with order asc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "asc"}
    rv = client.get("/admin/user", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "asc"), "should be sorted in ascending order"


def test_list_user_order_desc(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user
    Method: GET
    Assert: status_code = 200
    Description:
        Test list admin with order desc
    """
    headers = {"Authorization": "Bearer " + auth.token}
    params = {"orderBy": "id", "order": "desc"}
    rv = client.get("/admin/user", query_string=params, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)
    assert prove_order(body["response"], "desc"), "should be sorted in descending order"


def test_user_disabled(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user/disabled/<uid>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test disabled user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    user = search_user(client, auth, "user@common.com")
    rv = client.patch("/admin/user/disabled/" + user[0]["uid"], headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
    assert body["response"]["a"]["disabled"] is True, "should be disabled True"
    assert body["response"]["b"]["disabled"] is True, "should be disabled True"


def test_list_user_disabled(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user?disabled=true
    Method: GET
    Assert: status_code = 200
    Description:
        Test list user filter by disabled true
    """
    headers = {"Authorization": "Bearer " + auth.token}
    rv = client.get("/admin/user", query_string={"disabled": True}, headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_list)

    for item in body["response"]:
        assert item["disabled"] is True, "should be disabled True"


def test_user_enabled(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user/disabled/<uid>
    Method: PATCH
    Assert: status_code = 200
    Description:
        Test enabled user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    user = search_user(client, auth, "user@common.com")
    rv = client.patch("/admin/user/disabled/" + user[0]["uid"], headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema)
    assert body["response"]["a"]["disabled"] is False, "should be disabled False"
    assert body["response"]["b"]["disabled"] is False, "should be disabled False"


def test_user_delete(client, auth, login_admin, seed_speciality, seed_method):
    """
    Endpoint: /admin/user/<uid>
    Method: DELETE
    Assert: status_code = 200
    Description:
        Test delete user
    """
    headers = {"Authorization": "Bearer " + auth.token}
    user = search_user(client, auth, "user@common.com")
    rv = client.delete("/admin/user/" + user[0]["uid"], headers=headers)
    assert rv.status_code == 200, "should be status code 200"
    assert (
        rv.headers["Content-Type"] == "application/json"
    ), "should be content type application/json"
    body = loads(rv.data)
    validate(instance=body, schema=schema_delete)
