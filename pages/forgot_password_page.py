import allure
from locators.auth import ForgotPasswordLocators
from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    PATH = "/forgot-password"

    @allure.step("Ввести почту и нажать «Восстановить»")
    def recover(self, email):
        self.fill(ForgotPasswordLocators.EMAIL, email)
        self.click(ForgotPasswordLocators.SUBMIT)

    @allure.step("Проверить страницу восстановления пароля")
    def is_opened(self):
        return self.is_page(self.PATH, ForgotPasswordLocators.TITLE)
