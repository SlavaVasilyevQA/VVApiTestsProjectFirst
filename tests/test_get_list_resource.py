import httpx
from jsonschema import validate
from core.contracts import RESOURCE_DATA_SCHEME
import allure

BASE_URL = "https://reqres.in"
LIST_RESOURCE = "/api/unknown"
SINGLE_RESOURCE = "/api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "/api/unknown/23"

headers = {
    "x-api-key": "reqres-free-v1"
}


@allure.suite("Проверка запросов данных ресурсов")
class TestResources:
    @allure.title("Проверка получения списка ресурсов")
    def test_list_resource(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + LIST_RESOURCE}"):
            response = httpx.get(BASE_URL + LIST_RESOURCE, headers=headers)

        with allure.step(f"Проверка кода ответа по запросу: {BASE_URL + LIST_RESOURCE}"):
            assert response.status_code == 200

        data = response.json()["data"]
        for item in data:
            with allure.step("Проверка элементов из списка"):
                validate(item, RESOURCE_DATA_SCHEME)

    @allure.title("Проверка получения одного ресурса")
    def test_single_resource(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + SINGLE_RESOURCE}"):
            response = httpx.get(BASE_URL + SINGLE_RESOURCE, headers=headers)

        with allure.step(f"Проверка кода ответа по запросу: {BASE_URL + LIST_RESOURCE}"):
            assert response.status_code == 200

        data = response.json()["data"]

        with allure.step("Проверка валидации JSON-схемы"):
            validate(data, RESOURCE_DATA_SCHEME)

    @allure.title("Проверка не существующего ресурса")
    def test_single_resource_not_found(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + SINGLE_RESOURCE_NOT_FOUND}"):
            response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND, headers=headers)

        with allure.step(f"Проверка кода ответа по запросу: {BASE_URL + SINGLE_RESOURCE_NOT_FOUND}"):
            assert response.status_code == 404
