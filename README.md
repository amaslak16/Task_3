# Task_3 — UI-тесты Stellar Burgers

Python 3.12, pytest, Selenium и Allure. Один набор из 17 тестов запускается
в Chrome и Firefox. Целевой стенд: https://qa-stellarburgers.education-services.ru.

## Установка

Установите Google Chrome и Mozilla Firefox. Selenium Manager автоматически
подберёт драйверы; при первом запуске ему нужен доступ в интернет.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Для Windows: `py -m venv .venv`, затем `.venv\Scripts\activate`.

## Запуск

Из корня проекта, в активированном окружении:

```bash
python -m pytest --browser chrome --alluredir=allure-results/chrome --clean-alluredir
python -m pytest --browser firefox --alluredir=allure-results/firefox --clean-alluredir
```

По умолчанию используется Chrome без окна. `--headed` включает окно браузера.
Каждый тест получает новый драйвер; фикстура вызывает `quit()` после теста.
Параметр `--browser` имеет приоритет над переменной `BROWSER`. Неизвестное имя
браузера завершает запуск с понятной ошибкой до создания драйвера.

Примеры настройки:

```bash
BROWSER=firefox python -m pytest
STELLAR_BURGERS_URL=https://qa-stellarburgers.education-services.ru python -m pytest --browser chrome
python -m pytest --browser chrome --headed tests/test_password_recovery.py
```

Дополнительные переменные окружения: `UI_TIMEOUT` (25 секунд), `ORDER_TIMEOUT`
(60 секунд), `CHROME_BINARY`, `FIREFOX_BINARY`, `CHROMEDRIVER`, `GECKODRIVER`.
Последние четыре нужны только для нестандартного расположения браузеров/драйверов.
Для Firefox из Snap фабрика использует совместимые бинарники из установленного
пакета напрямую: это позволяет корректно завершать сервис без Snap-обёртки.
При недоступности стенда проверьте подключение
и VPN: тестам нужны HTTPS и WebSocket-соединения с выбранным адресом.

## Allure

Установите [Allure Commandline 2](https://allurereport.org/docs/v2/install/)
и Java. `allure-pytest` сохраняет результаты, а HTML формируется CLI.
Каталоги браузеров раздельные: `--clean-alluredir` очищает только каталог
выбранного прогона. Не смешивайте повторные прогоны без очистки.

```bash
allure generate allure-results/chrome -o allure-report/chrome --clean
allure generate allure-results/firefox -o allure-report/firefox --clean
allure open allure-report/chrome
allure open allure-report/firefox
```

Общий отчёт с отдельным параметром `browser`:

```bash
allure generate allure-results/chrome allure-results/firefox -o allure-report/combined --clean
allure open allure-report/combined
```

При ошибке прикладываются скриншот, DOM и URL; в Chrome также консоль
и список сетевых ошибок. Allure различает упавшие проверки (`failed`)
и ошибки подготовки/выполнения (`broken`). Фактические результаты,
ограничения стенда и архив для PR описаны в [TEST_RUN.md](TEST_RUN.md).

## Структура и проверки

- `tests/`: четыре тематических класса — восстановление пароля (3), кабинет (3),
  основной функционал (6), лента заказов (5).
- `pages/`: базовый Page Object и отдельный класс для каждой используемой страницы.
  Работа с WebDriver, ожиданиями, вкладками и DOM находится в `BasePage`.
- `locators/`: именованные локаторы по страницам.
- `browser_factory.py`: создание Chrome или Firefox.
- `config.py`, `data.py`: настройки, данные бургера, уникальный пользователь.
- `api_client.py`: API подготовки и удаления пользователей.
- `conftest.py`: браузер, предусловия, очистка данных, вложения Allure.

Вход выполняется через UI. Пользователь создаётся через API с уникальной почтой
и удаляется после теста, в том числе при падении проверки. Регистрация ожидает
HTTP 200, удаление — HTTP 202 и `success=true`: ответы проверены на текущем стенде.
При истечении токена очистка повторно входит через API. Сессия requests всегда
закрывается. API не используется для проверок UI и оформления заказов;
документированного удаления заказов нет.

Заказы создаются через UI для каждого нуждающегося в них теста. История, лента,
модальное окно и статистика сопоставляются с конкретным номером заказа.
Чтение номера ждёт исчезновения загрузки, чтобы не принять начальный `9999`
за результат. Проверки глобальных счётчиков требуют прирост минимум на 1
и наличие созданного заказа среди готовых: точное `+1` ненадёжно на общем
стенде с чужими заказами. Сценарий дневного счётчика выполняется в пределах
одного серверного дня; при пересечении полуночи его нужно запустить повторно.

Для короткого состояния «В работе» заранее открывается вторая вкладка ленты.
`MutationObserver` записывает только отображённые состояния соответствующего
DOM-списка; проверка ищет точный номер оформленного заказа. Запросы, ответы API
и состояние React не подменяются. HTML5 drag-and-drop отправляет стандартные
события `DragEvent` с `DataTransfer` одинаково в обоих браузерах: нативный
`ActionChains.drag_and_drop` здесь не переносит ингредиенты в Firefox.
Фиксированных задержек и автоматических повторов тестов нет.

Материалы и применённые замечания ревьюеров — в [REVIEW_NOTES.md](REVIEW_NOTES.md).
Работа подготовлена в ветке `develop3`; пул-реквест создаётся отдельно
по разрешению владельца.
