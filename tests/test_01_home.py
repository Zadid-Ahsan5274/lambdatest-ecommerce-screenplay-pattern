import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Open
from screenplay.ui.common import Common

pytestmark = [pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Home page")
class TestHome:
    @allure.title("Home page shows the store title")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_home_page_title(self, actor):
        actor.attempts_to(
            Open.route(Routes.HOME),
            Ensure.the_page().has_title_containing("Your Store"),
        )

    @allure.title("Home page lists featured products")
    @pytest.mark.smoke
    def test_home_page_lists_products(self, actor):
        actor.attempts_to(
            Open.route(Routes.HOME),
            Ensure.that(Common.PRODUCT_CARDS).is_present(),
        )