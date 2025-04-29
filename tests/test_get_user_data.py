import httpx
from jsonschema import validate
from core.contracts import USER_DATA_SCHEME
import allure

BASE_URL = "https://reqres.in"
LIST_USERS = "/api/users?page=2"
SINGLE_USER = "/api/users/2"
SINGLE_USER_NOT_FOUND = "/api/users/23"
EMAIL_ENDS = "@reqres.in"
AVATAR_ENDS = "-image.jpg"

headers = {
    "x-api-key": "reqres-free-v1"
}


@allure.suite("Проверка запросов данных пользователей")
class TestUsers:
    @allure.title("Проверка получения списка пользователей")
    def test_list_users(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + LIST_USERS}"):
            response = httpx.get(BASE_URL + LIST_USERS, headers=headers)

        with allure.step(f"Проверка кода ответа по запросу: {BASE_URL + LIST_USERS}"):
            assert response.status_code == 200

        data = response.json()["data"]
        for item in data:
            with allure.step("Проверка элементов из списка"):
                validate(item, USER_DATA_SCHEME)
                with allure.step("Проверка окончания Email адреса"):
                    assert item["email"].endswith(EMAIL_ENDS)
                with allure.step("Проверка наличия id в ссылке на аватарку"):
                    assert item["avatar"].endswith(str(item["id"]) + AVATAR_ENDS)

    @allure.title("Проверка получения одного пользователя")
    def test_single_user(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + SINGLE_USER}"):
            response = httpx.get(BASE_URL + SINGLE_USER, headers=headers)

        with allure.step(f"Проверка кода ответа по запросу: {BASE_URL + SINGLE_USER}"):
            assert response.status_code == 200

        data = response.json()["data"]
        with allure.step("Проверка окончания Email адреса"):
            assert data["email"].endswith(EMAIL_ENDS)
        with allure.step("Проверка наличия id в ссылке на аватарку"):
            assert data["avatar"].endswith(str(data["id"]) + AVATAR_ENDS)

    @allure.title("Проверка не существующего пользователя")
    def test_user_not_found(self):
        with allure.step(f"Делаем запрос по адресу: {BASE_URL + SINGLE_USER_NOT_FOUND}"):
            response = httpx.get(BASE_URL + SINGLE_USER_NOT_FOUND, headers=headers)

        with allure.step(f"Проверка кода ответа по запросу: {BASE_URL + SINGLE_USER_NOT_FOUND}"):
            assert response.status_code == 404
