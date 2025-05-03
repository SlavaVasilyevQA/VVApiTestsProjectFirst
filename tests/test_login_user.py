import json
import pytest
import httpx
from jsonschema import validate
from core.contracts import LOGIN_USER_SCHEME
import allure

BASE_URL = "https://reqres.in"
LOGIN_USER = "/api/login"

headers = {
    "x-api-key": "reqres-free-v1"
}

json_file = open("core/new_users_data_for_login.json")
users_data = json.load(json_file)


@allure.suite("Проверка входа пользователя")
class TestLoginUser:
    @allure.title("Проверка успешной авторизации пользователя")
    @pytest.mark.parametrize("users_data", users_data)
    def test_successful_login_user(self, users_data):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + LOGIN_USER}"):
            response = httpx.post(BASE_URL + LOGIN_USER, json=users_data, headers=headers)
            response_json = response.json()

        with allure.step(f"Проверка статус кода по адресу запроса: {BASE_URL + LOGIN_USER}"):
            assert response.status_code == 200

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, LOGIN_USER_SCHEME)

    @allure.title("Проверка не успешной авторизации пользователя")
    def test_unsuccessful_login_user(self):
        payload = {
            "email": "peter@klaven"
        }

        response_error = {
            "error": "Missing password"
        }

        with allure.step(f"Делаем запрос по адресу: {BASE_URL + LOGIN_USER}"):
            response = httpx.post(BASE_URL + LOGIN_USER, json=payload, headers=headers)

        with allure.step(f"Проверка статус кода по адресу запроса: {BASE_URL + LOGIN_USER}"):
            assert response.status_code == 400

        with allure.step(f"Проверка содержимого ответа"):
            assert json.loads(response.text) == response_error
