import allure
import requests

from config import settings
from errors import ConnectivityError, PreparationError


class UserApi:
    """API используется только для создания и удаления тестового пользователя."""

    def __init__(self):
        self.session = requests.Session()

    def _request(self, method, endpoint, **kwargs):
        try:
            response = self.session.request(
                method, f"{settings.base_url}/api/{endpoint}",
                timeout=settings.api_timeout, **kwargs,
            )
        except requests.RequestException as error:
            raise ConnectivityError(f"Нет связи с API: {method} {endpoint}: {error}") from error
        try:
            body = response.json()
        except ValueError as error:
            raise PreparationError(f"API {endpoint}: HTTP {response.status_code}, ответ не JSON") from error
        return response.status_code, body

    @allure.step("API: создать уникального тестового пользователя")
    def register(self, user):
        status, body = self._request("POST", "auth/register", json=user.registration_data())
        token = body.get("accessToken")
        if status != 200 or body.get("success") is not True or not token:
            if token:
                self.delete(token, user)
            raise PreparationError(f"Регистрация: ожидались HTTP 200, success=true и токен; HTTP {status}")
        return token

    def delete(self, token, user):
        with allure.step("API: удалить тестового пользователя"):
            status, body = self._request("DELETE", "auth/user", headers={"Authorization": token})
            if status == 401:
                login_status, login = self._request(
                    "POST", "auth/login", json={"email": user.email, "password": user.password}
                )
                if login_status != 200 or not login.get("accessToken"):
                    raise PreparationError("Не удалось войти для удаления тестового пользователя")
                status, body = self._request(
                    "DELETE", "auth/user", headers={"Authorization": login["accessToken"]}
                )
            if status != 202 or body.get("success") is not True:
                raise PreparationError(f"Удаление пользователя: ожидались HTTP 202 и success=true; HTTP {status}")

    def close(self):
        self.session.close()
