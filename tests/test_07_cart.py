import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Open
from screenplay.tasks.shopping import (
    AddToCart,
    ApplyCoupon,
    RemoveFirstItemFromCart,
    UpdateCartQuantity,
)
from screenplay.ui.common import Common
from screenplay.ui.shop_pages import CartPage
from config.catalog import Catalog

pytestmark = [pytest.mark.cart, pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Shopping cart")
class TestCart:
    @allure.title("A new session starts with an empty cart")
    def test_cart_is_empty_for_new_session(self, actor):
        actor.attempts_to(
            Open.route(Routes.CART),
            Ensure.that(Common.CONTENT).contains_text("Your shopping cart is empty!"),
        )

    @allure.title("Adding a product shows a success notification")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_to_cart_shows_notification(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone"),
            Ensure.that(Common.SUCCESS_TOAST).contains_text("You have added"),
        )

    @allure.title("A product added to the cart appears on the cart page")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_added_product_appears_in_cart(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone"),
            Open.route(Routes.CART),
            Ensure.that(CartPage.TABLE).contains_text("iPhone"),
        )

    @allure.title("Cart quantity can be updated")
    def test_update_cart_quantity(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone"),
            Open.route(Routes.CART),
            UpdateCartQuantity.to(3),
            Ensure.that(CartPage.QUANTITY).has_value("3"),
        )

    @allure.title("A product can be removed from the cart")
    def test_remove_product_from_cart(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone"),
            Open.route(Routes.CART),
            RemoveFirstItemFromCart.now(),
            Ensure.that(Common.CONTENT).contains_text("Your shopping cart is empty!"),
        )

    @allure.title("Two different products produce two cart rows")
    def test_two_products_in_cart(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone"),
            AddToCart.the_product("MacBook"),
            Open.route(Routes.CART),
            Ensure.that(CartPage.ITEM_ROWS).has_count(2),
        )

    @allure.title("Quantity chosen on the product page is carried into the cart")
    def test_add_with_custom_quantity(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone", quantity=3),
            Open.route(Routes.CART),
            Ensure.that(CartPage.QUANTITY).has_value("3"),
        )

    @allure.title("An invalid coupon is rejected")
    def test_invalid_coupon_is_rejected(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone"),
            Open.route(Routes.CART),
            ApplyCoupon.code("NOT-A-REAL-COUPON"),
            Ensure.that(Common.ERROR_MESSAGE).contains_text("Coupon is either invalid"),
        )