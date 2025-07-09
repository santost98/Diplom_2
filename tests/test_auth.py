"""Тесты авторизации пользователей"""

import pytest
import allure
from data.test_data import (
    VALID_USER_DATA, INVALID_USER_DATA_MISSING_EMAIL, 
    INVALID_USER_DATA_MISSING_PASSWORD, INVALID_USER_DATA_MISSING_NAME,
    VALID_LOGIN_DATA, INVALID_LOGIN_DATA_WRONG_PASSWORD, 
    INVALID_LOGIN_DATA_WRONG_EMAIL, EXPECTED_RESPONSES
)
from config import Config

@allure.epic("Авторизация пользователей")
class TestUserAuth:
    
    @allure.feature("Регистрация пользователя")
    @allure.story("Успешная регистрация уникального пользователя")
    @allure.title("Создание пользователя с валидными данными")
    def test_create_unique_user_success(self, api_client, unique_user_data):
        """Тест успешного создания уникального пользователя"""
        with allure.step("Отправка запроса на регистрацию"):
            response = api_client.register_user(unique_user_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "user" in response_data, "В ответе должно быть поле user"
            assert response_data["user"]["email"] == unique_user_data["email"], \
                "Email в ответе не совпадает с отправленным"
            assert response_data["user"]["name"] == unique_user_data["name"], \
                "Имя в ответе не совпадает с отправленным"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert "refreshToken" in response_data, "В ответе должен быть refreshToken"
    
    @allure.feature("Регистрация пользователя")
    @allure.story("Попытка регистрации уже существующего пользователя")
    @allure.title("Создание пользователя с уже существующим email")
    def test_create_user_already_exists(self, api_client, unique_user_data):
        """Тест попытки создания пользователя с уже существующим email"""
        with allure.step("Первичная регистрация пользователя"):
            response = api_client.register_user(unique_user_data)
            assert response.status_code == Config.STATUS_CODES["success"]
        
        with allure.step("Попытка повторной регистрации с тем же email"):
            response = api_client.register_user(unique_user_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["forbidden"], \
                f"Ожидался статус {Config.STATUS_CODES['forbidden']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
    
    @allure.feature("Регистрация пользователя")
    @allure.story("Регистрация без обязательного поля email")
    @allure.title("Создание пользователя без email")
    def test_create_user_missing_email(self, api_client):
        """Тест создания пользователя без email"""
        with allure.step("Отправка запроса на регистрацию без email"):
            response = api_client.register_user(INVALID_USER_DATA_MISSING_EMAIL)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["forbidden"], \
                f"Ожидался статус {Config.STATUS_CODES['forbidden']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
    
    @allure.feature("Регистрация пользователя")
    @allure.story("Регистрация без обязательного поля password")
    @allure.title("Создание пользователя без пароля")
    def test_create_user_missing_password(self, api_client):
        """Тест создания пользователя без пароля"""
        with allure.step("Отправка запроса на регистрацию без пароля"):
            response = api_client.register_user(INVALID_USER_DATA_MISSING_PASSWORD)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["forbidden"], \
                f"Ожидался статус {Config.STATUS_CODES['forbidden']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
    
    @allure.feature("Регистрация пользователя")
    @allure.story("Регистрация без обязательного поля name")
    @allure.title("Создание пользователя без имени")
    def test_create_user_missing_name(self, api_client):
        """Тест создания пользователя без имени"""
        with allure.step("Отправка запроса на регистрацию без имени"):
            response = api_client.register_user(INVALID_USER_DATA_MISSING_NAME)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["forbidden"], \
                f"Ожидался статус {Config.STATUS_CODES['forbidden']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
    
    @allure.feature("Авторизация пользователя")
    @allure.story("Успешная авторизация с корректными данными")
    @allure.title("Вход пользователя с правильными учетными данными")
    def test_login_user_success(self, api_client, unique_user_data):
        """Тест успешной авторизации пользователя"""
        with allure.step("Регистрация пользователя"):
            response = api_client.register_user(unique_user_data)
            assert response.status_code == Config.STATUS_CODES["success"]
        
        with allure.step("Отправка запроса на авторизацию"):
            login_data = {
                "email": unique_user_data["email"],
                "password": unique_user_data["password"]
            }
            response = api_client.login_user(login_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "user" in response_data, "В ответе должно быть поле user"
            assert response_data["user"]["email"] == unique_user_data["email"], \
                "Email в ответе не совпадает с отправленным"
            assert response_data["user"]["name"] == unique_user_data["name"], \
                "Имя в ответе не совпадает с отправленным"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert "refreshToken" in response_data, "В ответе должен быть refreshToken"
    
    @allure.feature("Авторизация пользователя")
    @allure.story("Неуспешная авторизация с неверным паролем")
    @allure.title("Вход пользователя с неправильным паролем")
    def test_login_user_wrong_password(self, api_client, unique_user_data):
        """Тест авторизации с неверным паролем"""
        with allure.step("Регистрация пользователя"):
            response = api_client.register_user(unique_user_data)
            assert response.status_code == Config.STATUS_CODES["success"]
        
        with allure.step("Отправка запроса на авторизацию с неверным паролем"):
            login_data = {
                "email": unique_user_data["email"],
                "password": "wrongpassword"
            }
            response = api_client.login_user(login_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["unauthorized"], \
                f"Ожидался статус {Config.STATUS_CODES['unauthorized']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
            assert "incorrect" in response_data["message"].lower(), \
                "Сообщение должно содержать информацию о неверных учетных данных"
    
    @allure.feature("Авторизация пользователя")
    @allure.story("Неуспешная авторизация с несуществующим email")
    @allure.title("Вход пользователя с несуществующим email")
    def test_login_user_wrong_email(self, api_client):
        """Тест авторизации с несуществующим email"""
        with allure.step("Отправка запроса на авторизацию с несуществующим email"):
            login_data = {
                "email": "nonexistent@example.com",
                "password": "password123"
            }
            response = api_client.login_user(login_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["unauthorized"], \
                f"Ожидался статус {Config.STATUS_CODES['unauthorized']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
            assert "incorrect" in response_data["message"].lower(), \
                "Сообщение должно содержать информацию о неверных учетных данных" 