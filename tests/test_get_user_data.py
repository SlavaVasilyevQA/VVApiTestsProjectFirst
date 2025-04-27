import httpx
from jsonschema import validate
from core.contracts import USER_DATA_SCHEME, RESOURCE_DATA_SCHEME

BASE_URL = "https://reqres.in"
LIST_USERS = "/api/users?page=2"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"
SINGLE_USER = "/api/users/2"
SINGLE_USER_NOT_FOUND = "/api/users/23"
LIST_RESOURCE = "/api/unknown"
SINGLE_RESOURCE = "/api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "/api/unknown/23"

headers = {
    "x-api-key": "reqres-free-v1"
}

def test_list_users():
    response = httpx.get(BASE_URL + LIST_USERS, headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]

    for item in data:
        validate(item, USER_DATA_SCHEME)
        assert item["email"].endswith(EMAIL_ENDS)
        assert item["avatar"].endswith(str(item["id"]) + AVATAR_ENDS)


def test_single_user():
    response = httpx.get(BASE_URL + SINGLE_USER, headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]

    assert data["email"].endswith(EMAIL_ENDS)
    assert data["avatar"].endswith(str(data["id"]) + AVATAR_ENDS)


def test_user_not_found():
    response = httpx.get(BASE_URL + SINGLE_USER_NOT_FOUND, headers=headers)
    assert response.status_code == 404


def test_list_resource():
    response = httpx.get(BASE_URL + LIST_RESOURCE, headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]

    for item in data:
        validate(item, RESOURCE_DATA_SCHEME)

def test_single_resource():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE, headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    validate(data, RESOURCE_DATA_SCHEME)

def test_single_resource_not_found():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND, headers=headers)
    assert response.status_code == 404