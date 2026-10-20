import allure
from selenium.webdriver.support import expected_conditions as EC
from config import settings
from locators.feed import FeedLocators as L
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    PATH = "/feed"

    @allure.step("Дождаться загрузки ленты и счётчиков")
    def wait_until_ready(self):
        self.visible(L.TOTAL)

    @allure.step("Проверить страницу ленты и статистику")
    def is_opened(self):
        return self.is_page(self.PATH, L.TITLE) and self.check(lambda _: (
            self.text(L.TOTAL).isdigit() and self.text(L.TODAY).isdigit()
        ))

    @allure.step("Проверить присутствие конкретного заказа в ленте")
    def contains_order(self, number):
        return self.check(EC.visibility_of_element_located(
            self.locator(L.ORDER, number=f"0{number}")
        ))

    @allure.step("Прочитать название конкретного заказа в ленте")
    def order_title(self, number):
        return self.text(self.locator(L.ORDER_TITLE, number=f"0{number}"))

    @allure.step("Открыть детали конкретного заказа")
    def open_order(self, number):
        self.click(self.locator(L.ORDER, number=f"0{number}"))

    @allure.step("Проверить номер, название и ингредиенты выбранного заказа в модальном окне")
    def details_match(self, order, title):
        return self.check(lambda _: (
            self.text(L.DETAIL_NUMBER) == f"#0{order.number}"
            and self.text(L.DETAIL_TITLE) == title
            and set(self.texts(L.DETAIL_INGREDIENTS)) == set(order.ingredients)
        ))

    @allure.step("Прочитать счётчик «Выполнено за всё время»")
    def total(self):
        return int(self.text(L.TOTAL))

    @allure.step("Прочитать счётчик «Выполнено за сегодня»")
    def today(self):
        return int(self.text(L.TODAY))

    def _completed_and_counter_increased(self, locator, before, number):
        return self.check(lambda _: (
            int(self.text(locator)) >= before + 1
            and self.element_is_visible(self.locator(L.ORDER, number=f"0{number}"))
            and self.element_is_visible(self.locator(L.READY_ORDER, number=f"0{number}"))
        ), timeout=settings.order_timeout)

    @allure.step("Проверить увеличение общего счётчика и готовность созданного заказа")
    def total_increased_for_order(self, before, number):
        return self._completed_and_counter_increased(L.TOTAL, before, number)

    @allure.step("Проверить увеличение дневного счётчика и готовность созданного заказа")
    def today_increased_for_order(self, before, number):
        return self._completed_and_counter_increased(L.TODAY, before, number)

    @allure.step("Открыть ленту во второй вкладке и наблюдать список «В работе»")
    def observe_in_progress_in_new_tab(self):
        original = self.get_tab()
        feed_tab = self.open_tab()
        self.open()
        self.wait_until_ready()
        self.watch_text(L.IN_PROGRESS)
        self.switch_tab(original)
        return feed_tab

    @allure.step("Проверить, что номер созданного заказа появился в разделе «В работе»")
    def order_was_in_progress(self, number, feed_tab):
        self.switch_tab(feed_tab)
        return self.check(lambda _: any(
            f"0{number}" in text.splitlines() for text in self.observed_texts()
        ), timeout=settings.order_timeout)
