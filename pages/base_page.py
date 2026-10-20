import allure
from selenium.common.exceptions import (
    ElementClickInterceptedException, NoSuchElementException,
    StaleElementReferenceException, TimeoutException, WebDriverException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings
from errors import ConnectivityError
from locators.common import HeaderLocators, ModalLocators


class BasePage:
    PATH = "/"

    def __init__(self, driver):
        self._driver = driver

    def wait(self, condition, timeout=None):
        return WebDriverWait(
            self._driver, timeout or settings.timeout,
            ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
        ).until(condition)

    def check(self, condition, timeout=None):
        try:
            return bool(self.wait(condition, timeout))
        except TimeoutException:
            return False

    def visible(self, locator):
        return self.wait(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait(lambda _: self._click_when_ready(locator))

    def _click_when_ready(self, locator):
        element = EC.element_to_be_clickable(locator)(self._driver)
        if not element:
            return False
        try:
            element.click()
            return True
        except (ElementClickInterceptedException, StaleElementReferenceException):
            return False

    def fill(self, locator, value):
        element = self.visible(locator)
        element.clear()
        element.send_keys(value)

    def text(self, locator):
        return self.visible(locator).text

    def dom_text(self, locator):
        return self._driver.find_element(*locator).get_attribute("textContent").strip()

    def texts(self, locator):
        return [element.text for element in self._driver.find_elements(*locator) if element.is_displayed()]

    def attribute(self, locator, name):
        return self.visible(locator).get_attribute(name)

    def element_is_visible(self, locator):
        try:
            return bool(EC.visibility_of_element_located(locator)(self._driver))
        except (NoSuchElementException, StaleElementReferenceException):
            return False

    @staticmethod
    def locator(template, **values):
        return template[0], template[1].format(**values)

    def is_page(self, path, locator):
        return self.check(lambda driver: (
            driver.current_url.rstrip("/") == f"{settings.base_url}{path}".rstrip("/")
            and EC.visibility_of_element_located(locator)(driver)
        ))

    @allure.step("Открыть страницу")
    def open(self):
        try:
            self._driver.get(f"{settings.base_url}{self.PATH}")
        except WebDriverException as error:
            if any(code in str(error) for code in ("ERR_NAME_NOT_RESOLVED", "ERR_CONNECTION", "dnsNotFound", "neterror")):
                raise ConnectivityError(f"Браузер не смог подключиться к {settings.base_url}") from error
            raise
        return self

    @allure.step("Перейти по ссылке «Личный кабинет»")
    def go_to_account(self):
        self.click(HeaderLocators.ACCOUNT)

    @allure.step("Перейти по ссылке «Конструктор»")
    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR)

    @allure.step("Перейти по ссылке «Лента заказов»")
    def go_to_feed(self):
        self.click(HeaderLocators.FEED)

    @allure.step("Закрыть модальное окно крестиком")
    def close_modal(self):
        self.click(ModalLocators.CLOSE)

    def modal_is_closed(self):
        return self.check(EC.invisibility_of_element_located(ModalLocators.OPEN_MODAL))

    def drag_and_drop(self, source_locator, target_locator):
        source = self.visible(source_locator)
        target = self.visible(target_locator)
        self._driver.execute_script("arguments[0].scrollIntoView({block:'center'});", source)
        self._driver.execute_script("""
            const source = arguments[0], target = arguments[1];
            const transfer = new DataTransfer();
            const send = (element, type) => element.dispatchEvent(new DragEvent(type, {
                bubbles: true, cancelable: true, dataTransfer: transfer,
            }));
            send(source, 'dragstart');
            send(target, 'dragenter');
            send(target, 'dragover');
            send(target, 'drop');
            send(source, 'dragend');
        """, source, target)

    def get_tab(self):
        return self._driver.current_window_handle

    def open_tab(self):
        self._driver.switch_to.new_window("tab")
        return self.get_tab()

    def switch_tab(self, handle):
        self._driver.switch_to.window(handle)

    def watch_text(self, locator):
        """Сохранять видимые состояния быстро меняющегося DOM в отдельной вкладке."""
        element = self.visible(locator)
        self._driver.execute_script("""
            window.uiObservedTexts = [arguments[0].innerText];
            window.uiObserver = new MutationObserver(() => {
                window.uiObservedTexts.push(arguments[0].innerText);
            });
            window.uiObserver.observe(arguments[0], {subtree: true, childList: true, characterData: true});
        """, element)

    def observed_texts(self):
        return self._driver.execute_script("return window.uiObservedTexts || [];")
