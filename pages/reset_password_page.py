import allure
from locators.auth import ResetPasswordLocators
from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    PATH = "/reset-password"

    @allure.step("Проверить форму нового пароля и кода из письма")
    def is_opened(self):
        return self.is_page(self.PATH, ResetPasswordLocators.SAVE) and self.check(
            lambda _: self.visible(ResetPasswordLocators.CODE).is_displayed()
        )

    @allure.step("Нажать кнопку показа/скрытия пароля")
    def toggle_password(self):
        self.click(ResetPasswordLocators.SHOW_PASSWORD)

    @allure.step("Проверить тип и подсветку поля пароля")
    def password_is_active(self, input_type):
        return self.check(lambda _: (
            self.attribute(ResetPasswordLocators.PASSWORD, "type") == input_type
            and "input_status_active" in self.attribute(ResetPasswordLocators.PASSWORD_WRAPPER, "class")
        ))

    @allure.step("Проверить скрытое неактивное поле пароля до клика")
    def password_is_initially_hidden(self):
        return self.check(lambda _: (
            self.attribute(ResetPasswordLocators.PASSWORD, "type") == "password"
            and "input_status_active" not in self.attribute(ResetPasswordLocators.PASSWORD_WRAPPER, "class")
        ))
