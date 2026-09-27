import allure
import pytest

from config.routes import Routes
from screenplay.ensure import Ensure
from screenplay.interactions import Open, SelectOption
from screenplay.questions import Prices, Texts
from screenplay.ui.common import Common
from screenplay.ui.shop_pages import CategoryPage
from config.catalog import Catalog

pytestmark = [pytest.mark.catalog, pytest.mark.regression]

DESKTOPS = 20


@allure.epic("Storefront")
@allure.feature("Catalog")
class TestCategory:
    @allure.title("Category '{name}' lists products")
    @pytest.mark.parametrize(
        "name,path",
        [("Desktops", Catalog.DESKTOPS_ID), ("Laptops", Catalog.LAPTOPS_ID), ("Tablets", Catalog.TABLETS_ID)],
    )
    def test_category_lists_products(self, actor, name, path):
        actor.attempts_to(
            Open.route(Routes.CATEGORY, path=path),
            Ensure.the_page().has_url_containing("product/category"),
            Ensure.that(Common.PRODUCT_CARDS).is_present(),
        )

    @allure.title("Products can be sorted by name (A-Z)")
    def test_sort_by_name_ascending(self, actor):
        actor.attempts_to(
            Open.route(Routes.CATEGORY, path=Catalog.DESKTOPS_ID),
            SelectOption.labelled("Name (A - Z)").from_(CategoryPage.SORT).and_wait_for_page_reload(),
            Ensure.the_page().has_url_containing("order=ASC"),
        )
        names = actor.asks_for(Texts.of(Common.PRODUCT_NAMES))
        assert names == sorted(names, key=str.lower)

    @allure.title("Products can be sorted by price (low to high)")
    def test_sort_by_price_ascending(self, actor):
        actor.attempts_to(
            Open.route(Routes.CATEGORY, path=DESKTOPS),
            SelectOption.labelled("Price (Low > High)").from_(CategoryPage.SORT).and_wait_for_page_reload(),
            Ensure.the_page().has_url_containing("sort=p.price"),
            Ensure.the_page().has_url_containing("order=ASC"),
        )
        prices = actor.asks_for(Prices.of(Common.PRODUCT_PRICES))
        assert prices and prices == sorted(prices)

    @allure.title("Products can be sorted by price (high to low)")
    def test_sort_by_price_descending(self, actor):
        actor.attempts_to(
            Open.route(Routes.CATEGORY, path=DESKTOPS),
            SelectOption.labelled("Price (High > Low)").from_(CategoryPage.SORT).and_wait_for_page_reload(),
            Ensure.the_page().has_url_containing("order=DESC"),
        )
        prices = actor.asks_for(Prices.of(Common.PRODUCT_PRICES))
        assert prices and prices == sorted(prices, reverse=True)