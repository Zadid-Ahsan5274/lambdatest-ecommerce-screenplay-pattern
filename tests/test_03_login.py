import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Click, Open
from screenplay.tasks.authentication import Login, Logout
from screenplay.ui.account_pages import AccountPage, LoginPage
from screenplay.ui.common import Common
from utils.data_factory import build_user, unique_email

pytestmark = [pytest.mark.login, pytest.mark.regression]

NO_MATCH = "No match for E-Mail Address and/or Password"


@allure.epic("Storefront")
@allure.feature("Authentication")
class TestLogin:
    @allure.title("A registered customer can log in")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, registered_actor):
        user = registered_actor.recall("user")
        registered_actor.attempts_to(
            Logout.now(),
            Login.as_(user),
            Ensure.the_page().has_url_containing("account/account"),
            Ensure.that(AccountPage.CONTAINER).is_visible(),
        )

    @allure.title("Wrong password is rejected")
    def test_login_with_wrong_password(self, registered_actor):
        user = registered_actor.recall("user")
        registered_actor.attempts_to(
            Logout.now(),
            Login.with_credentials(user.email, "WrongPass@999"),
            Ensure.that(Common.ERROR_MESSAGE).contains_text(NO_MATCH),
        )

    @allure.title("Unregistered e-mail is rejected")
    def test_login_with_unregistered_email(self, actor):
        actor.attempts_to(
            Login.with_credentials(unique_email("ghost"), "Whatever@123"),
            Ensure.that(Common.ERROR_MESSAGE).contains_text(NO_MATCH),
        )

    @allure.title("Empty credentials are blocked by client-side validation")
    def test_login_with_empty_credentials(self, actor):
        actor.attempts_to(
            Open.route(Routes.LOGIN),
            Click.on(LoginPage.LOGIN_BUTTON),
            # Required-field validation prevents the form from ever submitting
            Ensure.the_page().has_url_containing("account/login"),
        )

    @allure.title("Logging out ends the session")
    def test_logout_ends_session(self, registered_actor):
        registered_actor.attempts_to(
            Logout.now(),
            Ensure.that(Common.CONTENT).contains_text("Account Logout"),
            Open.route(Routes.ACCOUNT),
            Ensure.the_page().has_url_containing("account/login"),
        )

    @allure.title("Anonymous visitors are redirected to login from protected pages")
    def test_protected_page_redirects_to_login(self, actor):
        actor.attempts_to(
            Open.route(Routes.ACCOUNT),
            Ensure.the_page().has_url_containing("account/login"),
        )