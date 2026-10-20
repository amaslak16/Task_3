from selenium.webdriver.common.by import By


class ConstructorLocators:
    TITLE = (By.XPATH, '//h1[text()="Соберите бургер"]')
    INGREDIENT = (By.XPATH, '//a[starts-with(@href,"/ingredient/")][p[text()="{name}"]]')
    COUNTER = (By.XPATH, '//a[starts-with(@href,"/ingredient/")][p[text()="{name}"]]//p[contains(@class,"counter_counter__num")]')
    BASKET = (By.CSS_SELECTOR, 'section[class*="BurgerConstructor_basket__"]')
    BASKET_TEXT = (By.CSS_SELECTOR, 'section[class*="BurgerConstructor_basket__"] .constructor-element__text')
    SUBMIT_ORDER = (By.XPATH, '//button[text()="Оформить заказ"]')
    INGREDIENT_TITLE = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] h2')
    INGREDIENT_NAME = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] p.text_type_main-medium')
    INGREDIENT_STATS = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] li')
    ORDER_NUMBER = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] h2')
    ORDER_NUMBER_ANY_STATE = (By.CSS_SELECTOR, 'section h2[class*="Modal_modal__title_shadow"]')
    ORDER_CONFIRMATION = (By.XPATH, '//*[contains(@class,"Modal_modal_opened")]//p[text()="Ваш заказ начали готовить"]')
    ORDER_LOADING = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] img[alt="loading animation"]')
