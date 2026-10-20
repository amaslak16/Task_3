from selenium.webdriver.common.by import By


class FeedLocators:
    TITLE = (By.XPATH, '//h1[text()="Лента заказов"]')
    ORDER = (By.XPATH, '//a[starts-with(@href,"/feed/")][.//p[text()="#{number}"]]')
    ORDER_TITLE = (By.XPATH, '//a[starts-with(@href,"/feed/")][.//p[text()="#{number}"]]//h2')
    TOTAL = (By.XPATH, '//p[text()="Выполнено за все время:"]/following-sibling::p')
    TODAY = (By.XPATH, '//p[text()="Выполнено за сегодня:"]/following-sibling::p')
    IN_PROGRESS = (By.CSS_SELECTOR, '[class*="OrderFeed_orderListReady__"]')
    READY_ORDER = (By.XPATH, '//ul[contains(@class,"OrderFeed_orderList__") and not(contains(@class,"OrderFeed_orderListReady__"))]/li[normalize-space(.)="{number}"]')
    DETAIL_NUMBER = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] [class*="Modal_orderBox__"] > p:first-child')
    DETAIL_TITLE = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] h2')
    DETAIL_INGREDIENTS = (By.CSS_SELECTOR, '[class*="Modal_modal_opened"] li p.text_type_main-default')
