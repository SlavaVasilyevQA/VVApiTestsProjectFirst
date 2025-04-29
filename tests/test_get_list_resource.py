import httpx
from jsonschema import validate
from core.contracts import RESOURCE_DATA_SCHEME

BASE_URL = "https://reqres.in"
LIST_RESOURCE = "/api/unknown"
SINGLE_RESOURCE = "/api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "/api/unknown/23"

headers = {
    "x-api-key": "reqres-free-v1"
}


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
