import allure
import pytest

from screenplay.ensure import Ensure
from screenplay.questions import Texts
from screenplay.tasks.shopping import SearchFor, ViewProduct
from screenplay.ui.common import Common
from screenplay.ui.shop_pages import ProductPage
from config.catalog import Catalog

pytestmark = [pytest.mark.search, pytest.mark.regression]


@allure.epic("Storefront")
@allure.feature("Search")
class TestSearch:
    @allure.title("Searching for '{keyword}' returns matching products")
    @pytest.mark.parametrize("keyword", ["iphone", "macbook", "canon"])
    @pytest.mark.smoke
    def test_search_returns_matching_products(self, actor, keyword):
        actor.attempts_to(
            SearchFor.term(keyword),
            Ensure.that(Common.PRODUCT_CARDS).is_present(),
        )
        names = actor.asks_for(Texts.of(Common.PRODUCT_NAMES))
        assert names, "Expected at least one product"
        assert any(keyword in n.lower() for n in names), f"No result name contains '{keyword}': {names}"

     @allure.title("Search results heading reflects the keyword")
    def test_search_heading_reflects_keyword(self, actor):
        actor.attempts_to(
            SearchFor.term(Catalog.PRIMARY_PRODUCT.lower()),
            Ensure.the_page().has_url_containing("product/search"),
            Ensure.that(Common.CONTENT).contains_text(Catalog.PRIMARY_PRODUCT),
        )

    @allure.title("A nonsense keyword shows the empty-results message")
    def test_search_with_no_results(self, actor):
        actor.attempts_to(
            SearchFor.term(Catalog.NONSENSE_SEARCH_TERM),
            Ensure.that(Common.CONTENT).contains_text("There is no product that matches the search criteria"),
        )

    @allure.title("Search works from the header search box")
    def test_search_from_header_box(self, actor):
        actor.attempts_to(
            SearchFor.using_header_box(Catalog.PRIMARY_PRODUCT.lower()),
            Ensure.the_page().has_url_containing("product/search"),
            Ensure.that(Common.PRODUCT_CARDS).is_present(),
        )

    @allure.title("A search result opens its product page")
    def test_search_result_opens_product_page(self, actor):
        actor.attempts_to(
            ViewProduct.named(Catalog.PRIMARY_PRODUCT),
            Ensure.that(ProductPage.HEADING).contains_text(Catalog.PRIMARY_PRODUCT),
        )