import allure
from locators.auth import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    @allure.step("Войти через UI под тестовым пользователем")
    def login(self, user):
        self.fill(LoginLocators.EMAIL, user.email)
        self.fill(LoginLocators.PASSWORD, user.password)
        self.click(LoginLocators.SUBMIT)

    @allure.step("Нажать «Восстановить пароль»")
    def go_to_password_recovery(self):
        self.click(LoginLocators.FORGOT_PASSWORD)

    @allure.step("Проверить форму входа")
    def is_opened(self):
        return self.is_page(self.PATH, LoginLocators.TITLE)
