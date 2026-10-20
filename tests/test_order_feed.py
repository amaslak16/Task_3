import allure


@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("Клик по конкретному заказу открывает его номер, название и состав")
    def test_open_order_details(self, pages, created_order):
        pages.constructor.go_to_feed()
        title = pages.feed.order_title(created_order.number)
        pages.feed.open_order(created_order.number)
        assert pages.feed.details_match(created_order, title), "Детали не совпали с выбранным заказом"

    @allure.title("Заказ пользователя из истории присутствует в общей ленте")
    def test_history_order_appears_in_feed(self, pages, created_order):
        pages.constructor.go_to_account()
        pages.profile.go_to_history()
        title = pages.history.order_title(created_order.number)
        pages.history.go_to_feed()
        assert pages.feed.contains_order(created_order.number), "Заказ из истории отсутствует в ленте"
        assert pages.feed.order_title(created_order.number) == title, "Названия заказа в истории и ленте различаются"

    @allure.title("Новый заказ увеличивает счётчик «Выполнено за всё время»")
    def test_total_counter_increases(self, pages, authenticated):
        pages.constructor.go_to_feed()
        before = pages.feed.total()
        pages.feed.go_to_constructor()
        pages.constructor.build_burger()
        pages.constructor.submit_order()
        number = pages.constructor.order_number()
        pages.constructor.close_modal()
        pages.constructor.go_to_feed()
        assert pages.feed.total_increased_for_order(before, number), "Общий счётчик не увеличился или созданный заказ не появился среди готовых"

    @allure.title("Новый заказ увеличивает счётчик «Выполнено за сегодня»")
    def test_today_counter_increases(self, pages, authenticated):
        pages.constructor.go_to_feed()
        before = pages.feed.today()
        pages.feed.go_to_constructor()
        pages.constructor.build_burger()
        pages.constructor.submit_order()
        number = pages.constructor.order_number()
        pages.constructor.close_modal()
        pages.constructor.go_to_feed()
        assert pages.feed.today_increased_for_order(before, number), "Дневной счётчик не увеличился или созданный заказ не появился среди готовых"

    @allure.title("Номер оформленного заказа появляется в разделе «В работе»")
    def test_created_order_is_in_progress(self, pages, authenticated):
        feed_tab = pages.feed.observe_in_progress_in_new_tab()
        pages.constructor.build_burger()
        pages.constructor.submit_order()
        number = pages.constructor.order_number()
        assert pages.feed.order_was_in_progress(number, feed_tab), f"Заказ {number} не появился в разделе «В работе»"
