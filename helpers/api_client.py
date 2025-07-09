"""API клиент для работы с Stellar Burgers API"""

import requests
from config import Config

class StellarBurgersAPI:
    """Клиент для работы с API Stellar Burgers"""
    
    def __init__(self):
        self.base_url = Config.BASE_URL
        self.session = requests.Session()
        self.access_token = None
    
    def set_access_token(self, token):
        """Устанавливает токен доступа для авторизованных запросов"""
        self.access_token = token
        if token:
            # Проверяем, есть ли уже префикс Bearer в токене
            if token.startswith("Bearer "):
                self.session.headers.update({"Authorization": token})
            else:
                self.session.headers.update({"Authorization": f"Bearer {token}"})
        else:
            self.session.headers.pop("Authorization", None)
    
    def _make_request(self, method, endpoint, **kwargs):
        """Выполняет HTTP запрос"""
        url = f"{self.base_url}{endpoint}"
        return self.session.request(method, url, **kwargs)
    
    def register_user(self, user_data):
        """Регистрация пользователя"""
        return self._make_request("POST", Config.ENDPOINTS["register"], json=user_data)
    
    def login_user(self, login_data):
        """Авторизация пользователя"""
        return self._make_request("POST", Config.ENDPOINTS["login"], json=login_data)
    
    def get_user_info(self):
        """Получение информации о пользователе"""
        return self._make_request("GET", Config.ENDPOINTS["user"])
    
    def update_user_info(self, user_data):
        """Обновление информации о пользователе"""
        return self._make_request("PATCH", Config.ENDPOINTS["user"], json=user_data)
    
    def create_order(self, order_data):
        """Создание заказа"""
        return self._make_request("POST", Config.ENDPOINTS["orders"], json=order_data)
    
    def get_orders(self):
        """Получение списка заказов пользователя"""
        return self._make_request("GET", Config.ENDPOINTS["orders"])
    
    def get_ingredients(self):
        """Получение списка ингредиентов"""
        return self._make_request("GET", Config.ENDPOINTS["ingredients"]) 