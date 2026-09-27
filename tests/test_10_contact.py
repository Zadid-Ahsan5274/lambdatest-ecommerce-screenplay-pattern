import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Click, Open
from screenplay.tasks.account import SubmitContactForm
from screenplay.ui.common import Common
from screenplay.ui.shop_pages import ContactPage
from utils.data_factory import unique_email

pytestmark = [pytest.mark.contact, pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Contact us")
class TestContact:
    @allure.title("A valid enquiry is sent successfully")
    def test_submit_valid_enquiry(self, actor):
        actor.attempts_to(
            SubmitContactForm.with_details(
                "Test Tester", unique_email("contact"), "Hello, this is an automated enquiry from the QA suite."
            ),
            Ensure.that(Common.CONTENT).contains_text("Your enquiry has been successfully sent"),
        )

    @allure.title("An empty contact form shows validation errors")
    def test_empty_contact_form(self, actor):
        actor.attempts_to(
            Open.route(Routes.CONTACT),
            Click.on(ContactPage.SUBMIT),
            Ensure.that(Common.FIELD_ERRORS).has_element_with_text("Name must be between 3 and 32 characters!"),
        )

    @allure.title("A too-short enquiry is rejected")
    def test_short_enquiry_is_rejected(self, actor):
        actor.attempts_to(
            SubmitContactForm.with_details("Test Tester", unique_email("contact"), "short"),
            Ensure.that(Common.FIELD_ERRORS).has_element_with_text("Enquiry must be between 10 and 3000 characters!"),
        )