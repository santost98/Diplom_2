"""Генератор пользователей для тестов"""

import random
import string
import time

class UserGenerator:
    """Класс для генерации уникальных пользователей"""
    
    @staticmethod
    def generate_unique_email():
        """Генерирует уникальный email"""
        timestamp = int(time.time() * 1000)
        random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"test_{random_string}_{timestamp}@example.com"
    
    @staticmethod
    def generate_unique_name():
        """Генерирует уникальное имя пользователя"""
        timestamp = int(time.time() * 1000)
        random_string = ''.join(random.choices(string.ascii_letters, k=6))
        return f"TestUser_{random_string}_{timestamp}"
    
    @staticmethod
    def generate_password():
        """Генерирует пароль"""
        return "password123"
    
    @staticmethod
    def generate_unique_user_data():
        """Генерирует полные данные уникального пользователя"""
        return {
            "email": UserGenerator.generate_unique_email(),
            "password": UserGenerator.generate_password(),
            "name": UserGenerator.generate_unique_name()
        }
    
    @staticmethod
    def generate_user_data_with_custom_email(email):
        """Генерирует данные пользователя с указанным email"""
        return {
            "email": email,
            "password": UserGenerator.generate_password(),
            "name": UserGenerator.generate_unique_name()
        } 