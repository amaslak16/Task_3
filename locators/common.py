from selenium.webdriver.common.by import By


class HeaderLocators:
    CONSTRUCTOR = (By.CSS_SELECTOR, 'header nav a[href="/"]')
    FEED = (By.CSS_SELECTOR, 'header a[href="/feed"]')
    ACCOUNT = (By.CSS_SELECTOR, 'header a[href="/account"]')


class ModalLocators:
    OPEN_MODAL = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"]')
    CLOSE = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] button[class*="Modal_modal__close"]')
