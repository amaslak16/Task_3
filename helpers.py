from dataclasses import dataclass

from pages.constructor_page import ConstructorPage
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage
from pages.order_history_page import OrderHistoryPage
from pages.profile_page import ProfilePage
from pages.reset_password_page import ResetPasswordPage


@dataclass(frozen=True)
class Pages:
    constructor: ConstructorPage
    login: LoginPage
    forgot: ForgotPasswordPage
    reset: ResetPasswordPage
    profile: ProfilePage
    history: OrderHistoryPage
    feed: OrderFeedPage

    @classmethod
    def create(cls, driver):
        return cls(*(page(driver) for page in (
            ConstructorPage, LoginPage, ForgotPasswordPage, ResetPasswordPage,
            ProfilePage, OrderHistoryPage, OrderFeedPage,
        )))
