import httpx
import allure

BASE_URL = "https://reqres.in"
DELETE_USER = "/api/users/2"

headers = {
    "x-api-key": "reqres-free-v1"
}


@allure.suite("Удаление пользовательских данных")
class TestDeleteUser:
    @allure.title("Удаление пользователя")
    def test_delete_user(self):
        with allure.step(f"Отправка запроса на удаление пользователя: {BASE_URL + DELETE_USER}"):
            response = httpx.delete(BASE_URL + DELETE_USER, headers=headers)

        with allure.step(f"Проверка статус кода ответа по запросу: {BASE_URL + DELETE_USER}"):
            assert response.status_code == 204
