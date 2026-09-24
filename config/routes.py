from __future__ import annotations
from urllib.parse import urlencode
from config.settings import settings

class Routes:
    HOME = "common/home"
    LOGIN = "account/login"
    REGISTER = "account/register"
    LOGOUT = "account/logout"
    CONTACT = "information/contact"
    CHECKOUT = "checkout/checkout"
    CART = "checkout/cart"
    COMPARE = "product/compare"
    PRODUCT = "product/product"
    CATEGORY = "product/category"
    SEARCH = "product/search"
    WISHLIST = "account/wishlist"
    ORDERS = "account/order"
    PASSWORD = "account/password"
    EDIT_ACCOUNT = "account/edit"
    ACCOUNT = "account/account"

def url_for(route:str,**params) -> str:
    query = urlencode({"route":route,**params},safe="/")
    return f"{settings.base_url}/index.php?{query}"
