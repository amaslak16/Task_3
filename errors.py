class ConnectivityError(RuntimeError):
    """Нет связи со стендом или API; это не ошибка UI-проверки."""


class PreparationError(RuntimeError):
    """Не выполнена подготовка окружения или тестовых данных."""
