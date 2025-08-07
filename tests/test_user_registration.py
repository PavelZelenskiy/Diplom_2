import pytest
import requests
import allure
from ..helpers import generate_user_data
from ..urls import AUTH_REGISTER

@allure.feature("Регистрация пользователя")
class TestUserRegistration:
    @allure.story("Успешная регистрация")
    @allure.title("Регистрация нового пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_unique_user(self):
        with allure.step("Подготовка тестовых данных пользователя"):
            user_data = generate_user_data()
        
        with allure.step("Отправка запроса на регистрацию"):
            response = requests.post(AUTH_REGISTER, json=user_data)
            allure.attach(str(response.json()), name="Response", attachment_type=allure.attachment_type.JSON)
        
        with allure.step("Проверка успешной регистрации"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "accessToken" in response.json()

    @allure.story("Ошибки регистрации")
    @allure.title("Попытка регистрации существующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user(self, registered_user):
        with allure.step("Повторная регистрация того же пользователя"):
            response = requests.post(AUTH_REGISTER, json=registered_user)
        
        with allure.step("Проверка ошибки"):
            assert response.status_code == 403
            assert response.json()["message"] == "User already exists"

    @allure.story("Ошибки регистрации")
    @allure.title("Регистрация без обязательного поля: {missing_field}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        with allure.step(f"Подготовка данных без поля {missing_field}"):
            user_data = generate_user_data()
            del user_data[missing_field]
        
        with allure.step("Отправка запроса"):
            response = requests.post(AUTH_REGISTER, json=user_data)
        
        with allure.step("Проверка ошибки"):
            assert response.status_code == 403
            assert response.json()["message"] == "Email, password and name are required fields"