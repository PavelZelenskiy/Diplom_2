import pytest
import requests
import allure
from ..urls import AUTH_LOGIN

@allure.feature("Авторизация пользователя")
class TestUserLogin:
    @allure.story("Успешная авторизация")
    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_success(self, registered_user):
        with allure.step("Подготовка данных для входа"):
            login_data = {
                "email": registered_user["email"],
                "password": registered_user["password"]
            }
        
        with allure.step("Отправка запроса на авторизацию"):
            response = requests.post(AUTH_LOGIN, json=login_data)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Проверка успешного входа"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.story("Ошибки авторизации")
    @allure.title("Попытка входа с неверными данными: {incorrect_data}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("incorrect_data", [
        {"email": "wrong@example.com", "password": "wrong"},
        {"password": "password"},  # нет email
        {"email": "test@example.com"}  # нет пароля
    ], ids=["wrong_credentials", "missing_email", "missing_password"])
    def test_login_failure(self, incorrect_data):
        with allure.step("Подготовка неверных данных"):
            test_data = incorrect_data
        
        with allure.step("Отправка запроса"):
            response = requests.post(AUTH_LOGIN, json=test_data)
        
        with allure.step("Проверка ошибки"):
            assert response.status_code == 401
            assert response.json()["message"] == "email or password are incorrect"