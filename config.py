import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv(
        "STELLAR_BURGERS_URL", "https://qa-stellarburgers.education-services.ru"
    ).rstrip("/")
    timeout: int = int(os.getenv("UI_TIMEOUT", "25"))
    order_timeout: int = int(os.getenv("ORDER_TIMEOUT", "60"))
    api_timeout: int = 30


settings = Settings()
