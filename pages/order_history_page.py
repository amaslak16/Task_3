import allure
from selenium.webdriver.support import expected_conditions as EC
from locators.account import AccountLocators, HistoryLocators
from pages.base_page import BasePage


class OrderHistoryPage(BasePage):
    PATH = "/account/order-history"

    @allure.step("Проверить выбранный раздел «История заказов»")
    def is_opened(self):
        return self.is_page(self.PATH, AccountLocators.ACTIVE_HISTORY_LINK)

    @allure.step("Проверить конкретный заказ в истории")
    def contains_order(self, number):
        return self.check(EC.visibility_of_element_located(
            self.locator(HistoryLocators.ORDER, number=f"0{number}")
        ))

    @allure.step("Прочитать название конкретного заказа в истории")
    def order_title(self, number):
        return self.text(self.locator(HistoryLocators.ORDER_TITLE, number=f"0{number}"))
