"""Тесты работы с пользователями"""

import pytest
import allure
from helpers.user_generator import UserGenerator
from config import Config

@allure.epic("Пользователи")
class TestUsers:
    
    @allure.feature("Информация о пользователе")
    @allure.story("Получение информации авторизованного пользователя")
    @allure.title("Получение данных пользователя")
    def test_get_user_info_success(self, authorized_user):
        """Тест получения информации о пользователе"""
        api_client = authorized_user["api_client"]
        user_data = authorized_user["user_data"]
        
        with allure.step("Отправка запроса на получение информации о пользователе"):
            response = api_client.get_user_info()
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "user" in response_data, "В ответе должно быть поле user"
            assert response_data["user"]["email"] == user_data["email"], \
                "Email в ответе не совпадает с ожидаемым"
            assert response_data["user"]["name"] == user_data["name"], \
                "Имя в ответе не совпадает с ожидаемым"
    
    @allure.feature("Информация о пользователе")
    @allure.story("Получение информации неавторизованного пользователя")
    @allure.title("Получение данных пользователя без авторизации")
    def test_get_user_info_without_auth(self, api_client):
        """Тест получения информации о пользователе без авторизации"""
        with allure.step("Отправка запроса на получение информации без авторизации"):
            response = api_client.get_user_info()
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["unauthorized"], \
                f"Ожидался статус {Config.STATUS_CODES['unauthorized']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message"
    
    @allure.feature("Обновление пользователя")
    @allure.story("Обновление информации авторизованного пользователя")
    @allure.title("Обновление данных пользователя")
    def test_update_user_info_success(self, authorized_user):
        """Тест обновления информации о пользователе"""
        api_client = authorized_user["api_client"]
        
        with allure.step("Подготовка новых данных пользователя"):
            new_user_data = {
                "name": UserGenerator.generate_unique_name(),
                "email": UserGenerator.generate_unique_email()
            }
        
        with allure.step("Отправка запроса на обновление информации"):
            response = api_client.update_user_info(new_user_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["success"], \
                f"Ожидался статус {Config.STATUS_CODES['success']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "user" in response_data, "В ответе должно быть поле user"
            assert response_data["user"]["email"] == new_user_data["email"], \
                "Email в ответе не совпадает с обновленным"
            assert response_data["user"]["name"] == new_user_data["name"], \
                "Имя в ответе не совпадает с обновленным"
    
    @allure.feature("Обновление пользователя")
    @allure.story("Обновление информации неавторизованного пользователя")
    @allure.title("Обновление данных пользователя без авторизации")
    def test_update_user_info_without_auth(self, api_client):
        """Тест обновления информации о пользователе без авторизации"""
        with allure.step("Подготовка данных для обновления"):
            new_user_data = {
                "name": UserGenerator.generate_unique_name(),
                "email": UserGenerator.generate_unique_email()
            }
        
        with allure.step("Отправка запроса на обновление без авторизации"):
            response = api_client.update_user_info(new_user_data)
        
        with allure.step("Проверка статус кода"):
            assert response.status_code == Config.STATUS_CODES["unauthorized"], \
                f"Ожидался статус {Config.STATUS_CODES['unauthorized']}, получен {response.status_code}"
        
        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "В ответе должно быть поле message" 