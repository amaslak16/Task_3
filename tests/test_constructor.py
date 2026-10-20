import allure
from data import BurgerData


@allure.feature("Основной функционал")
class TestConstructor:
    @allure.title("Ссылка «Конструктор» возвращает из ленты к ингредиентам")
    def test_navigate_to_constructor(self, pages):
        pages.feed.open()
        pages.feed.go_to_constructor()
        assert pages.constructor.is_opened(), "Не открылся конструктор с ингредиентами"

    @allure.title("Ссылка «Лента заказов» открывает список и счётчики")
    def test_navigate_to_order_feed(self, pages):
        pages.constructor.open()
        pages.constructor.go_to_feed()
        assert pages.feed.is_opened(), "Не открылась лента со статистикой"

    @allure.title("Клик по ингредиенту показывает его название и пищевую ценность")
    def test_open_ingredient_details(self, pages):
        pages.constructor.open()
        pages.constructor.open_ingredient(BurgerData.BUN)
        assert pages.constructor.ingredient_details_are_shown(BurgerData.BUN), "Открылись неверные детали ингредиента"

    @allure.title("Крестик закрывает окно деталей ингредиента")
    def test_close_ingredient_details(self, pages):
        pages.constructor.open()
        pages.constructor.open_ingredient(BurgerData.BUN)
        pages.constructor.close_modal()
        assert pages.constructor.modal_is_closed(), "Окно ингредиента осталось открытым"

    @allure.title("Добавление соуса увеличивает его счётчик с 0 до 1 и 2")
    def test_ingredient_counter_increases(self, pages):
        pages.constructor.open()
        assert pages.constructor.ingredient_count_is(BurgerData.SAUCE, 0), "Начальный счётчик не равен нулю"
        pages.constructor.add_ingredient(BurgerData.SAUCE)
        assert pages.constructor.ingredient_count_is(BurgerData.SAUCE, 1), "После первого добавления счётчик не равен 1"
        pages.constructor.add_ingredient(BurgerData.SAUCE)
        assert pages.constructor.ingredient_count_is(BurgerData.SAUCE, 2), "После второго добавления счётчик не равен 2"

    @allure.title("Авторизованный пользователь оформляет заказ через UI")
    def test_authorized_user_places_order(self, pages, authenticated):
        pages.constructor.build_burger()
        pages.constructor.submit_order()
        assert pages.constructor.order_is_confirmed(), "Нет подтверждения с реальным номером заказа"
        number = pages.constructor.order_number()
        pages.constructor.close_modal()
        pages.constructor.go_to_account()
        pages.profile.go_to_history()
        assert pages.history.contains_order(number), "Оформленный заказ не сохранён в истории пользователя"
