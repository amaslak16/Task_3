import allure
from locators.account import AccountLocators
from pages.base_page import BasePage


class ProfilePage(BasePage):
    PATH = "/account/profile"

    @allure.step("Проверить профиль конкретного пользователя")
    def shows_user(self, user):
        return self.is_page(self.PATH, AccountLocators.PROFILE_LINK) and self.check(lambda _: (
            self.attribute(AccountLocators.NAME, "value") == user.name
            and self.attribute(AccountLocators.EMAIL, "value") == user.email
        ))

    @allure.step("Перейти в «Историю заказов»")
    def go_to_history(self):
        self.click(AccountLocators.HISTORY_LINK)

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.click(AccountLocators.LOGOUT)
