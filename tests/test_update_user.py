import httpx
from jsonschema import validate
from core.contracts import UPDATE_USER_DATA_SCHEME
import allure
import datetime

BASE_URL = "https://reqres.in"
UPDATE_USER = "/api/users/2"

headers = {
    "x-api-key": "reqres-free-v1"
}


@allure.suite("Обновление пользовательских данных")
class TestUpdateUser:
    @allure.title("Обновление пользователя")
    def test_full_update_user(self):
        payload = {
            "name": "morpheus",
            "job": "zion resident"
        }

        with allure.step(f"Отправка запроса на обновление пользователя: {BASE_URL + UPDATE_USER}"):
            response = httpx.put(BASE_URL + UPDATE_USER, json=payload, headers=headers)
            response_json = response.json()

        with allure.step(f"Проверка статус кода ответа по запросу: {BASE_URL + UPDATE_USER}"):
            assert response.status_code == 200

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, UPDATE_USER_DATA_SCHEME)

        with allure.step("Проверка поля \"name\""):
            assert response_json["name"] == payload["name"]

        with allure.step("Проверка поля \"job\""):
            assert response_json["job"] == payload["job"]

        updation_date = response_json["updatedAt"].replace("T", " ")
        current_date = str(datetime.datetime.utcnow())

        with allure.step("Проверка даты обновления пользователя"):
            assert updation_date[0:16] == current_date[0:16]

    @allure.title("Частичное обновление пользователя")
    def test_partial_update_user(self):
        payload = {
            "name": "morpheus",
            "job": "zion resident123"
        }

        with allure.step(f"Отправка запроса на частичное обновление пользователя: {BASE_URL + UPDATE_USER}"):
            response = httpx.patch(BASE_URL + UPDATE_USER, json=payload, headers=headers)
            response_json = response.json()

        with allure.step(f"Проверка статус кода ответа по запросу: {BASE_URL + UPDATE_USER}"):
            assert response.status_code == 200

        with allure.step("Валидация JSON-схемы"):
            validate(response_json, UPDATE_USER_DATA_SCHEME)

        with allure.step("Проверка поля \"name\""):
            assert response_json["name"] == payload["name"]

        with allure.step("Проверка поля \"job\""):
            assert response_json["job"] == payload["job"]

        updation_date = response_json["updatedAt"].replace("T", " ")
        current_date = str(datetime.datetime.utcnow())

        with allure.step("Проверка даты частичного обновления пользователя"):
            assert updation_date[0:16] == current_date[0:16]
