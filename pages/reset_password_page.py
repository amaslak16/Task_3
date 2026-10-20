import allure
from locators.auth import ResetPasswordLocators
from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    PATH = "/reset-password"

    @allure.step("Проверить форму нового пароля и кода из письма")
    def is_opened(self):
        return self.is_page(self.PATH, ResetPasswordLocators.SAVE) and self.check(
            lambda _: self.element_is_visible(ResetPasswordLocators.PASSWORD)
            and self.element_is_visible(ResetPasswordLocators.CODE)
        )

    @allure.step("Нажать значок показа пароля")
    def show_password(self):
        self.click(ResetPasswordLocators.SHOW_PASSWORD)

    @allure.step("Проверить тип, фокус и подсветку поля пароля")
    def password_is_active(self):
        return self.check(lambda _: (
            self.attribute(ResetPasswordLocators.PASSWORD, "type") == "text"
            and self.element_is_focused(ResetPasswordLocators.PASSWORD)
            and "input_status_active" in self.attribute(ResetPasswordLocators.PASSWORD_WRAPPER, "class").split()
        ))
