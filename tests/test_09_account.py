import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Open
from screenplay.tasks.account import ChangePassword, UpdateProfile
from screenplay.tasks.authentication import Login, Logout
from screenplay.ui.account_pages import AccountPage, EditAccountPage
from screenplay.ui.common import Common

pytestmark = [pytest.mark.account, pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("My account")
class TestAccount:
    @allure.title("Profile changes are persisted")
    def test_edit_account_information(self, registered_actor):
        registered_actor.attempts_to(
            UpdateProfile.first_name("Updated"),
            Open.route(Routes.EDIT_ACCOUNT),
            Ensure.that(EditAccountPage.FIRST_NAME).has_value("Updated"),
        )

    @allure.title("After changing the password the customer can log in with the new one")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_change_password_and_relogin(self, registered_actor):
        user = registered_actor.recall("user")
        new_password = "NewPass@789"
        registered_actor.attempts_to(
            ChangePassword.to(new_password),
            Logout.now(),
            Login.with_credentials(user.email, new_password),
            Ensure.the_page().has_url_containing("account/account"),
            Ensure.that(AccountPage.CONTAINER).is_visible(),
        )

    @allure.title("A new customer has no order history")
    def test_order_history_is_empty_for_new_customer(self, registered_actor):
        registered_actor.attempts_to(
            Open.route(Routes.ORDERS),
            Ensure.that(Common.CONTENT).contains_text("You have not made any previous orders!"),
        )