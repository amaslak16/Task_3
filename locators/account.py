from selenium.webdriver.common.by import By


class AccountLocators:
    NAME = (By.CSS_SELECTOR, 'input[name="Name"]')
    EMAIL = (By.CSS_SELECTOR, 'input[type="text"][name="name"]')
    PROFILE_LINK = (By.CSS_SELECTOR, 'a[href="/account/profile"][aria-current="page"]')
    HISTORY_LINK = (By.CSS_SELECTOR, 'a[href="/account/order-history"]')
    ACTIVE_HISTORY_LINK = (By.CSS_SELECTOR, 'a[href="/account/order-history"][aria-current="page"]')
    LOGOUT = (By.XPATH, '//button[text()="Выход"]')


class HistoryLocators:
    ORDER = (By.XPATH, '//a[starts-with(@href,"/account/order-history/")][.//p[text()="#{number}"]]')
    ORDER_TITLE = (By.XPATH, '//a[starts-with(@href,"/account/order-history/")][.//p[text()="#{number}"]]//h2')
