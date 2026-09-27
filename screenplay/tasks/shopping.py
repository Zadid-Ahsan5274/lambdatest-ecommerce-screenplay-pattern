from __future__ import annotations

from config.routes import Routes
from screenplay.core.interfaces import Task
from screenplay.ensure import Ensure
from screenplay.interactions import Click, Enter, Open, Press
from screenplay.ui.common import Common
from screenplay.ui.shop_pages import CartPage, ProductPage


class SearchFor(Task):
    def __init__(self, term: str, via_header: bool = False) -> None:
        self._term = term
        self._via_header = via_header

    @classmethod
    def term(cls, term: str) -> "SearchFor":
        return cls(term)

    @classmethod
    def using_header_box(cls, term: str) -> "SearchFor":
        return cls(term, via_header=True)

    def __str__(self) -> str:
        how = "the header search box" if self._via_header else "the search page"
        return f"searches for '{self._term}' using {how}"

    def perform_as(self, actor) -> None:
        if self._via_header:
            actor.attempts_to(
                Open.route(Routes.HOME),
                Enter.text(self._term).into(Common.SEARCH_INPUT),
                Press.key("Enter").on(Common.SEARCH_INPUT),
            )
        else:
            actor.attempts_to(Open.route(Routes.SEARCH, search=self._term))


class ViewProduct(Task):
    def __init__(self, name: str) -> None:
        self._name = name

    @classmethod
    def named(cls, name: str) -> "ViewProduct":
        return cls(name)

    def __str__(self) -> str:
        return f"opens the '{self._name}' product page"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            SearchFor.term(self._name),
            Click.on(Common.PRODUCT_LINK.of(name=self._name)),
            Ensure.the_page().has_url_containing("product/product"),
        )


class AddToCart(Task):
    def __init__(self, name: str, quantity: int = 1) -> None:
        self._name = name
        self._quantity = quantity

    @classmethod
    def the_product(cls, name: str, quantity: int = 1) -> "AddToCart":
        return cls(name, quantity)

    def __str__(self) -> str:
        return f"adds {self._quantity} x '{self._name}' to the cart"

    def perform_as(self, actor) -> None:
        actor.attempts_to(ViewProduct.named(self._name))
        if self._quantity != 1:
            actor.attempts_to(Enter.text(str(self._quantity)).into(ProductPage.QUANTITY))
        actor.attempts_to(Click.on(ProductPage.ADD_TO_CART).and_wait_for_response_from("cart", "add"))


class AddToWishlist(Task):
    def __init__(self, name: str) -> None:
        self._name = name

    @classmethod
    def the_product(cls, name: str) -> "AddToWishlist":
        return cls(name)

    def __str__(self) -> str:
        return f"adds '{self._name}' to the wish list"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            ViewProduct.named(self._name),
            Click.on(ProductPage.WISHLIST).and_wait_for_response_from("wishlist", "add"),
        )


class AddToCompare(Task):
    def __init__(self, name: str) -> None:
        self._name = name

    @classmethod
    def the_product(cls, name: str) -> "AddToCompare":
        return cls(name)

    def __str__(self) -> str:
        return f"adds '{self._name}' to the comparison"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            ViewProduct.named(self._name),
            Click.on(ProductPage.COMPARE).and_wait_for_response_from("compare", "add"),
        )


class UpdateCartQuantity(Task):
    def __init__(self, quantity: int) -> None:
        self._quantity = quantity

    @classmethod
    def to(cls, quantity: int) -> "UpdateCartQuantity":
        return cls(quantity)

    def __str__(self) -> str:
        return f"updates the first cart item quantity to {self._quantity}"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Enter.text(str(self._quantity)).into(CartPage.QUANTITY),
            Click.on(CartPage.UPDATE).and_wait_for_response_from("cart", "edit"),
            Open.route(Routes.CART),
        )


class RemoveFirstItemFromCart(Task):
    @classmethod
    def now(cls) -> "RemoveFirstItemFromCart":
        return cls()

    def __str__(self) -> str:
        return "removes the first item from the cart"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Click.on(CartPage.REMOVE).and_wait_for_response_from("cart", "remove"),
            Open.route(Routes.CART),
        )


class ApplyCoupon(Task):
    def __init__(self, code: str) -> None:
        self._code = code

    @classmethod
    def code(cls, code: str) -> "ApplyCoupon":
        return cls(code)

    def __str__(self) -> str:
        return f"applies coupon '{self._code}'"

    def perform_as(self, actor) -> None:
        if not CartPage.COUPON_INPUT.resolve_for(actor).is_visible():
            actor.attempts_to(Click.on(CartPage.COUPON_TOGGLE))
        actor.attempts_to(
            Enter.text(self._code).into(CartPage.COUPON_INPUT),
            Click.on(CartPage.COUPON_APPLY),
        )