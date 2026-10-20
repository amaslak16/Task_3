import allure


@allure.feature("Восстановление пароля")
class TestPasswordRecovery:
    @allure.title("Кнопка «Восстановить пароль» открывает форму восстановления")
    def test_open_password_recovery(self, pages):
        pages.login.open()
        pages.login.go_to_password_recovery()
        assert pages.forgot.is_opened(), "Не открылась форма восстановления пароля"

    @allure.title("Отправка почты открывает форму нового пароля и кода")
    def test_submit_recovery_email(self, pages, registered_user):
        pages.forgot.open()
        pages.forgot.recover(registered_user.email)
        assert pages.reset.is_opened(), "После отправки почты не появилась форма сброса пароля"

    @allure.title("Клик по значку пароля активирует и подсвечивает поле")
    def test_password_visibility_activates_field(self, reset_form):
        reset_form.show_password()
        assert reset_form.password_is_active(), "Клик не показал пароль или не установил фокус и подсветку"
