import allure
from selenium.webdriver.support import expected_conditions as EC
from config import settings
from data import BurgerData
from locators.constructor import ConstructorLocators as L
from pages.base_page import BasePage


class ConstructorPage(BasePage):
    @allure.step("Дождаться загрузки конструктора и ингредиентов")
    def wait_until_ready(self):
        self.visible(self.locator(L.INGREDIENT, name=BurgerData.BUN))

    @allure.step("Проверить страницу конструктора")
    def is_opened(self):
        return self.is_page(self.PATH, L.TITLE) and self.check(
            EC.visibility_of_element_located(self.locator(L.INGREDIENT, name=BurgerData.BUN))
        )

    @allure.step("Открыть детали ингредиента «{name}»")
    def open_ingredient(self, name):
        self.click(self.locator(L.INGREDIENT, name=name))

    @allure.step("Проверить детали выбранного ингредиента")
    def ingredient_details_are_shown(self, name):
        return self.check(lambda _: (
            self.text(L.INGREDIENT_TITLE) == "Детали ингредиента"
            and self.text(L.INGREDIENT_NAME) == name
            and len(self.texts(L.INGREDIENT_STATS)) == 4
        ))

    @allure.step("Добавить ингредиент «{name}» перетаскиванием")
    def add_ingredient(self, name):
        self.drag_and_drop(self.locator(L.INGREDIENT, name=name), L.BASKET)

    @allure.step("Проверить счётчик ингредиента «{name}»: {expected}")
    def ingredient_count_is(self, name, expected):
        return self.check(lambda _: int(self.text(self.locator(L.COUNTER, name=name))) == expected)

    @allure.step("Собрать бургер из булки и соуса")
    def build_burger(self):
        self.wait_until_ready()
        self.add_ingredient(BurgerData.BUN)
        self.add_ingredient(BurgerData.SAUCE)
        self.wait(lambda _: len(self.texts(L.BASKET_TEXT)) == 3)

    @allure.step("Нажать «Оформить заказ»")
    def submit_order(self):
        self._previous_order_number = self.dom_text(L.ORDER_NUMBER_ANY_STATE)
        self._order_loading_seen = False
        self.click(L.SUBMIT_ORDER)

    def _order_completed(self, _):
        if self.element_is_visible(L.ORDER_LOADING):
            self._order_loading_seen = True
            return False
        number = self.text(L.ORDER_NUMBER)
        return (
            (number != self._previous_order_number or self._order_loading_seen)
            and number.isdigit() and int(number) > 0
            and self.text(L.ORDER_CONFIRMATION) == "Ваш заказ начали готовить"
        )

    @allure.step("Проверить подтверждение оформления и положительный номер заказа")
    def order_is_confirmed(self):
        return self.check(self._order_completed, timeout=settings.order_timeout)

    @allure.step("Прочитать номер оформленного заказа")
    def order_number(self):
        self.wait(self._order_completed, settings.order_timeout)
        return int(self.text(L.ORDER_NUMBER))
