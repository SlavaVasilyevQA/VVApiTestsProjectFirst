import json
import pytest
import httpx
from jsonschema import validate
from core.contracts import REGISTER_USER_SCHEME
import allure

BASE_URL = "https://reqres.in"
REGISTER_USER = "/api/register"

headers = {
    "x-api-key": "reqres-free-v1"
}

json_file = open("core/new_users_data_for_registration.json")
users_data = json.load(json_file)


@allure.suite("Проверка регистрации пользователя")
class TestRegisterUser:
    @allure.title("Проверка успешной регистрации пользователя")
    @pytest.mark.parametrize("users_data", users_data)
    def test_successful_register_user(self, users_data):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + REGISTER_USER}"):
            response = httpx.post(BASE_URL + REGISTER_USER, json=users_data, headers=headers)
            response_json = response.json()

        with allure.step(f"Проверка статус кода по адресу запроса: {BASE_URL + REGISTER_USER}"):
            assert response.status_code == 200

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, REGISTER_USER_SCHEME)

    @allure.title("Проверка не успешной регистрации пользователя")
    def test_unsuccessful_register_user(self):
        payload = {
            "email": "sydney@fife"
        }

        response_error = {
            "error": "Missing password"
        }

        with allure.step(f"Делаем запрос по адресу: {BASE_URL + REGISTER_USER}"):
            response = httpx.post(BASE_URL + REGISTER_USER, json=payload, headers=headers)

        with allure.step(f"Проверка статус кода по адресу запроса: {BASE_URL + REGISTER_USER}"):
            assert response.status_code == 400

        with allure.step(f"Проверка содержимого ответа"):
            assert json.loads(response.text) == response_error
