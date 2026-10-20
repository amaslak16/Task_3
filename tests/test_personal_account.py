import allure


@allure.feature("Личный кабинет")
class TestPersonalAccount:
    @allure.title("Личный кабинет открывает профиль вошедшего пользователя")
    def test_open_personal_account(self, pages, authenticated):
        pages.constructor.go_to_account()
        assert pages.profile.shows_user(authenticated), "В профиле нет имени и почты созданного пользователя"

    @allure.title("История заказов показывает заказ текущего пользователя")
    def test_open_order_history(self, pages, created_order):
        pages.constructor.go_to_account()
        pages.profile.go_to_history()
        assert pages.history.is_opened(), "Не выбран раздел «История заказов»"
        assert pages.history.contains_order(created_order.number), "В истории нет созданного заказа"

    @allure.title("Выход закрывает доступ к личному кабинету")
    def test_logout(self, pages, authenticated):
        pages.constructor.go_to_account()
        pages.profile.logout()
        assert pages.login.is_opened(), "После выхода не появилась форма входа"
        pages.login.go_to_account()
        assert pages.login.is_opened(), "После выхода личный кабинет остался доступен"
