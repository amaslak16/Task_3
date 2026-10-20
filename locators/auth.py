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
    PASSWORD = (By.CSS_SELECTOR, 'form input[name="Введите новый пароль"]')
    PASSWORD_WRAPPER = (By.XPATH, '//form//input[@name="Введите новый пароль"]/parent::div[contains(concat(" ", normalize-space(@class), " "), " input ")]')
    SHOW_PASSWORD = (By.XPATH, '//form//input[@name="Введите новый пароль"]/parent::div/div[contains(concat(" ", normalize-space(@class), " "), " input__icon ")]')
    CODE = (By.XPATH, '//label[text()="Введите код из письма"]/following-sibling::input')
    SAVE = (By.XPATH, '//button[text()="Сохранить"]')
