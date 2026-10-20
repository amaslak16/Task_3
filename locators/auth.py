from selenium.webdriver.common.by import By


class LoginLocators:
    TITLE = (By.XPATH, '//h2[text()="Вход"]')
    EMAIL = (By.CSS_SELECTOR, 'form input[type="text"]')
    PASSWORD = (By.CSS_SELECTOR, 'form input[type="password"]')
    SUBMIT = (By.XPATH, '//button[text()="Войти"]')
    FORGOT_PASSWORD = (By.CSS_SELECTOR, 'a[href="/forgot-password"]')


class ForgotPasswordLocators:
    TITLE = (By.XPATH, '//h2[text()="Восстановление пароля"]')
    EMAIL = (By.CSS_SELECTOR, 'form input[type="text"]')
    SUBMIT = (By.XPATH, '//button[text()="Восстановить"]')


class ResetPasswordLocators:
    PASSWORD = (By.XPATH, '//label[text()="Введите новый пароль"]/following-sibling::input')
    PASSWORD_WRAPPER = (By.XPATH, '//label[text()="Введите новый пароль"]/parent::div')
    SHOW_PASSWORD = (By.CSS_SELECTOR, 'form .input__icon')
    CODE = (By.XPATH, '//label[text()="Введите код из письма"]/following-sibling::input')
    SAVE = (By.XPATH, '//button[text()="Сохранить"]')
