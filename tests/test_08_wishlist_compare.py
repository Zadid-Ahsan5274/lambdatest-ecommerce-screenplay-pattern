import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Click, Open
from screenplay.tasks.shopping import AddToCompare, AddToWishlist
from screenplay.ui.common import Common
from screenplay.ui.shop_pages import ComparePage, WishlistPage

pytestmark = [pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Wish list")
class TestWishlist:
    @allure.title("A logged-in customer can add a product to the wish list")
    @pytest.mark.wishlist
    def test_add_product_to_wishlist(self, registered_actor):
        registered_actor.attempts_to(
            AddToWishlist.the_product("iPhone"),
            Open.route(Routes.WISHLIST),
            Ensure.that(Common.CONTENT).contains_text("iPhone"),
        )

    @allure.title("A product can be removed from the wish list")
    @pytest.mark.wishlist
    def test_remove_product_from_wishlist(self, registered_actor):
        registered_actor.attempts_to(
            AddToWishlist.the_product("iPhone"),
            Open.route(Routes.WISHLIST),
            Click.on(WishlistPage.REMOVE),
            Ensure.that(Common.CONTENT).contains_text("Your wish list is empty"),
        )


@allure.epic("Storefront")
@allure.feature("Product comparison")
class TestCompare:
    @allure.title("A product added to comparison appears on the compare page")
    @pytest.mark.compare
    def test_add_product_to_compare(self, actor):
        actor.attempts_to(
            AddToCompare.the_product("iPhone"),
            Open.route(Routes.COMPARE),
            Ensure.that(ComparePage.TABLE).contains_text("iPhone"),
        )

    @allure.title("Compare page is empty by default")
    @pytest.mark.compare
    def test_compare_page_empty_by_default(self, actor):
        actor.attempts_to(
            Open.route(Routes.COMPARE),
            Ensure.that(Common.CONTENT).contains_text("You have not chosen any products to compare."),
        )