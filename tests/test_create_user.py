import httpx
from jsonschema import validate
from core.contracts import CREATE_USER_DATA_SCHEME
import allure
import datetime

BASE_URL = "https://reqres.in"
CREATE_USER = "/api/users"

headers = {
    "x-api-key": "reqres-free-v1"
}


@allure.suite("Проверка создания пользователя")
class TestCreateUser:
    @allure.title("Проверка создания пользователя с именем и должностью")
    def test_create_user_with_name_and_job(self):
        payload = {
            "name": "morpheus",
            "job": "leader"
        }

        with allure.step(f"Делаем запрос по адресу: {BASE_URL + CREATE_USER}"):
            response = httpx.post(BASE_URL + CREATE_USER, json=payload, headers=headers)
            response_json = response.json()

        with allure.step(f"Проверка статус кода по адресу запроса: {BASE_URL + CREATE_USER}"):
            assert response.status_code == 201

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, CREATE_USER_DATA_SCHEME)

        with allure.step("Проверка поля \"name\""):
            assert response_json["name"] == payload["name"]

        with allure.step("Проверка поля \"job\""):
            assert response_json["job"] == payload["job"]

        creation_date = response_json["createdAt"].replace("T", " ")
        current_date = str(datetime.datetime.utcnow())

        with allure.step("Проверка даты создания пользователя"):
            assert creation_date[0:16] == current_date[0:16]

    @allure.title("Проверка создания пользователя без имени")
    def test_create_user_without_name(self):
        payload = {
            "job": "leader"
        }

        with allure.step(f"Делаем запрос по адресу: {BASE_URL + CREATE_USER}"):
            response = httpx.post(BASE_URL + CREATE_USER, json=payload, headers=headers)
            response_json = response.json()

        with allure.step(f"Проверка статус кода по адресу запроса: {BASE_URL + CREATE_USER}"):
            assert response.status_code == 201

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, CREATE_USER_DATA_SCHEME)

        with allure.step("Проверка поля \"job\""):
            assert response_json["job"] == payload["job"]

        creation_date = response_json["createdAt"].replace("T", " ")
        current_date = str(datetime.datetime.utcnow())

        with allure.step("Проверка даты создания пользователя"):
            assert creation_date[0:16] == current_date[0:16]

    @allure.title("Проверка создания пользователя без должности")
    def test_create_user_without_job(self):
        payload = {
            "name": "morpheus"
        }

        with allure.step(f"Делаем запрос по адресу: {BASE_URL + CREATE_USER}"):
            response = httpx.post(BASE_URL + CREATE_USER, json=payload, headers=headers)
            response_json = response.json()

        with allure.step(f"Проверка статус кода по адресу запроса: {BASE_URL + CREATE_USER}"):
            assert response.status_code == 201

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, CREATE_USER_DATA_SCHEME)

        creation_date = response_json["createdAt"].replace("T", " ")
        current_date = str(datetime.datetime.utcnow())

        with allure.step("Проверка даты создания пользователя"):
            assert creation_date[0:16] == current_date[0:16]
