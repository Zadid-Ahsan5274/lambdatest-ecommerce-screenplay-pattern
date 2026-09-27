import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Click, Open
from screenplay.tasks.authentication import Logout, Register
from screenplay.ui.account_pages import AccountPage, RegisterPage
from screenplay.ui.common import Common
from utils.data_factory import build_user

pytestmark = [pytest.mark.registration, pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Registration")
class TestRegistration:
    @allure.title("A new customer can register with valid details")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_register_with_valid_details(self, actor):
        actor.attempts_to(
            Register.as_new_customer(build_user()),
            Ensure.that(RegisterPage.SUCCESS_HEADING).contains_text("Your Account Has Been Created"),
            Ensure.the_page().has_url_containing("account/success"),
        )

    @allure.title("Registration requires accepting the privacy policy")
    def test_register_without_privacy_policy(self, actor):
        actor.attempts_to(
            Register.as_new_customer(build_user()).without_accepting_privacy_policy(),
            Ensure.that(Common.ERROR_MESSAGE).contains_text("Privacy Policy"),
        )

    @allure.title("Submitting an empty registration form shows field errors")
    def test_register_with_empty_form(self, actor):
        actor.attempts_to(
            Open.route(Routes.REGISTER),
            Click.on(RegisterPage.CONTINUE),
            Ensure.that(Common.FIELD_ERRORS).has_element_with_text("First Name must be between 1 and 32 characters!"),
            Ensure.that(Common.FIELD_ERRORS).has_element_with_text("Last Name must be between 1 and 32 characters!"),
        )

    @allure.title("Mismatched password confirmation is rejected")
    def test_register_with_mismatched_passwords(self, actor):
        user = build_user(confirm_password="Different@123")
        actor.attempts_to(
            Register.as_new_customer(user),
            Ensure.that(Common.FIELD_ERRORS).has_element_with_text("Password confirmation does not match password!"),
        )

    @allure.title("An already-registered e-mail cannot be reused")
    def test_register_with_existing_email(self, actor):
        user = build_user()
        actor.attempts_to(
            Register.as_new_customer(user),
            Ensure.that(RegisterPage.SUCCESS_HEADING).contains_text("Your Account Has Been Created"),
            Logout.now(),
            Register.as_new_customer(build_user(email=user.email)),
            Ensure.that(Common.ERROR_MESSAGE).contains_text("E-Mail Address is already registered!"),
        )

    @allure.title("A too-short password is rejected")
    def test_register_with_short_password(self, actor):
        actor.attempts_to(
            Register.as_new_customer(build_user(password="ab")),
            Ensure.that(Common.FIELD_ERRORS).has_element_with_text("Password must be between 4 and 20 characters!"),
        )