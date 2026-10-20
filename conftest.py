import json
import os
from pathlib import Path

import allure
import pytest
from selenium.common.exceptions import WebDriverException

from api_client import UserApi
from browser_factory import BrowserFactory
from config import settings
from data import Order, User
from errors import PreparationError
from helpers import Pages


def pytest_addoption(parser):
    parser.addoption("--browser", default=os.getenv("BROWSER", "chrome"),
                     help="Браузер: chrome или firefox (по умолчанию BROWSER либо chrome)")
    parser.addoption("--headed", action="store_true", help="Показывать окно браузера")


def pytest_configure(config):
    browser = config.getoption("--browser")
    if browser not in BrowserFactory.SUPPORTED:
        raise pytest.UsageError(f"Неизвестный браузер '{browser}'. Доступны: chrome, firefox.")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    try:
        instance = BrowserFactory.create(browser, headless=not request.config.getoption("--headed"))
    except WebDriverException as error:
        raise PreparationError(f"Не удалось запустить {browser}: {error}") from error
    allure.dynamic.label("browser", browser)
    allure.dynamic.parameter("browser", browser)
    yield instance
    instance.quit()


@pytest.fixture
def pages(driver):
    return Pages.create(driver)


@pytest.fixture
def registered_user():
    api = UserApi()
    user = User.unique()
    token = None
    try:
        token = api.register(user)
        yield user
    finally:
        try:
            if token:
                api.delete(token, user)
        finally:
            api.close()


@pytest.fixture
def authenticated(pages, registered_user):
    pages.login.open()
    pages.login.login(registered_user)
    pages.constructor.wait_until_ready()
    return registered_user


@pytest.fixture
def created_order(pages, authenticated):
    pages.constructor.build_burger()
    pages.constructor.submit_order()
    number = pages.constructor.order_number()
    pages.constructor.close_modal()
    return Order(number)


@pytest.fixture
def reset_form(pages, registered_user):
    pages.forgot.open()
    pages.forgot.recover(registered_user.email)
    if not pages.reset.is_opened():
        raise PreparationError("Форма сброса пароля недоступна после отправки почты; проверка подсветки не может начаться")
    return pages.reset


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        instance = item.funcargs.get("driver")
        if instance:
            try:
                allure.attach(instance.get_screenshot_as_png(), "Экран при ошибке", allure.attachment_type.PNG)
                allure.attach(instance.page_source, "DOM при ошибке", allure.attachment_type.HTML)
                allure.attach(instance.current_url, "URL при ошибке", allure.attachment_type.TEXT)
                if instance.capabilities["browserName"] == "chrome":
                    allure.attach(json.dumps(instance.get_log("browser"), ensure_ascii=False),
                                  "Консоль браузера", allure.attachment_type.JSON)
                    failures = []
                    for entry in instance.get_log("performance"):
                        message = json.loads(entry["message"])["message"]
                        if message["method"] == "Network.responseReceived":
                            response = message["params"]["response"]
                            if response["status"] >= 400:
                                failures.append({"url": response["url"].split("?")[0], "status": response["status"]})
                        elif message["method"] == "Network.loadingFailed":
                            failures.append({"error": message["params"]["errorText"]})
                    allure.attach(json.dumps(failures, ensure_ascii=False),
                                  "Ошибки сетевых запросов", allure.attachment_type.JSON)
            except WebDriverException:
                pass


def pytest_sessionfinish(session, exitstatus):
    results = session.config.getoption("allure_report_dir", default=None)
    if results:
        directory = Path(results)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "environment.properties").write_text(
            f"Browser={session.config.getoption('--browser')}\nBase.URL={settings.base_url}\n",
            encoding="utf-8",
        )
        (directory / "categories.json").write_text(json.dumps([
            {"name": "Подключение к приложению или API", "matchedStatuses": ["broken"],
             "traceRegex": ".*ConnectivityError.*"},
            {"name": "Подготовка браузера или данных", "matchedStatuses": ["broken"],
             "traceRegex": ".*PreparationError.*"},
            {"name": "Проверка поведения приложения", "matchedStatuses": ["failed"]},
        ], ensure_ascii=False), encoding="utf-8")
