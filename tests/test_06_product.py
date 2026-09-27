import allure
import pytest

from config.catalog import Catalog
from screenplay.questions import Value
from screenplay.ensure import Ensure
from screenplay.tasks.shopping import ViewProduct
from screenplay.ui.shop_pages import ProductPage

pytestmark = [pytest.mark.product, pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Product details")
class TestProductPage:
    @allure.title("Product page shows the product name")
    def test_product_page_shows_name(self, actor):
        actor.attempts_to(
            ViewProduct.named(Catalog.PRIMARY_PRODUCT),
            Ensure.that(ProductPage.HEADING).contains_text(Catalog.PRIMARY_PRODUCT),
        )

    @allure.title("Product page offers an Add to Cart button")
    def test_product_page_has_add_to_cart(self, actor):
        actor.attempts_to(
            ViewProduct.named(Catalog.SECONDARY_PRODUCT),
            Ensure.that(ProductPage.ADD_TO_CART).is_visible(),
        )

    @allure.title("Default quantity is 1")
    def test_default_quantity_is_valid(self, actor):
        actor.attempts_to(ViewProduct.named(Catalog.PRIMARY_PRODUCT))
        qty = actor.asks_for(Value.of(ProductPage.QUANTITY))
        assert qty.isdigit() and int(qty) >= 1, f"Unexpected default quantity: {qty!r}"