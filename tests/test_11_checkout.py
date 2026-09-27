import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Click, Open
from screenplay.tasks.shopping import AddToCart
from screenplay.ui.shop_pages import CartPage, CheckoutPage

pytestmark = [pytest.mark.checkout, pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Checkout")
class TestCheckout:
    @allure.title("Checkout with an empty cart redirects back to the cart")
    def test_empty_cart_checkout_redirects_to_cart(self, actor):
        actor.attempts_to(
            Open.route(Routes.CHECKOUT),
            Ensure.the_page().has_url_containing("checkout/cart"),
        )

    @allure.title("A visitor with items in the cart can reach checkout and sees Guest Checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_visitor_reaches_checkout_from_cart(self, actor):
        actor.attempts_to(
            AddToCart.the_product("iPhone"),
            Open.route(Routes.CART),
            Click.on(CartPage.CHECKOUT),
            Ensure.the_page().has_url_containing("checkout/checkout"),
            Ensure.that(CheckoutPage.GUEST_OPTION).is_visible(),
        )