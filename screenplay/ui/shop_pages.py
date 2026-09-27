from screenplay.ui.target import Target


class CategoryPage:
    SORT = Target("Sort-by dropdown", "select[id^='input-sort']", first=True)


class ProductPage:
    HEADING = Target("Product heading", "#product-product h1", first=True)
    QUANTITY = Target("Quantity field", "#product-product input[name='quantity']", first=True)
    ADD_TO_CART = Target("Add to Cart button", "#product-product button:has-text('Add to Cart'):visible", first=True)
    WISHLIST = Target("Add to Wish List button", "#product-product [title='Add to Wish List']:visible", first=True)
    COMPARE = Target("Compare this Product button", "#product-product [title='Compare this Product']:visible", first=True)


class CartPage:
    TABLE = Target("Cart table", "#checkout-cart form table", first=True)
    ITEM_ROWS = Target("Cart item rows", "#checkout-cart form table tbody tr")
    QUANTITY = Target("Cart quantity field", "#checkout-cart input[name^='quantity']", first=True)
    UPDATE = Target(
        "Update cart button",
        "#checkout-cart form button[title='Update'], #checkout-cart form button[data-original-title='Update'],"
        " #checkout-cart form button:has(i.fa-sync), #checkout-cart form button:has(i.fa-refresh)",
        first=True,
    )
    REMOVE = Target(
        "Remove item button",
        "#checkout-cart [title='Remove'], #checkout-cart [data-original-title='Remove'],"
        " #checkout-cart button:has(i.fa-times-circle)",
        first=True,
    )
    COUPON_TOGGLE = Target("Use Coupon Code toggle", "a:has-text('Use Coupon Code')", first=True)
    COUPON_INPUT = Target("Coupon input", "#input-coupon", first=True)
    COUPON_APPLY = Target("Apply coupon button", "#button-coupon", first=True)
    CHECKOUT = Target("Checkout button", "#checkout-cart a[href*='checkout/checkout']:visible", first=True)


class WishlistPage:
    REMOVE = Target("Remove from wish list", "#account-wishlist a[href*='remove='], #account-wishlist [title='Remove']", first=True)


class ComparePage:
    TABLE = Target("Compare table", "#product-compare table", first=True)


class ContactPage:
    NAME = Target("Contact name field", "#input-name")
    EMAIL = Target("Contact E-Mail field", "#input-email")
    ENQUIRY = Target("Enquiry field", "#input-enquiry")
    SUBMIT = Target("Submit button", "input[value='Submit'], button:has-text('Submit')", first=True)
    # Match on structure, not guessed copy
    SUCCESS_ALERT = Target("Success alert", ".alert-success, .alert.alert-success", first=True)


class CheckoutPage:
    # The exact label copy wasn't "Guest Checkout" in this theme — match on the page reaching
    # its checkout-options step instead of a specific literal string.
    CHECKOUT_HEADING = Target("Checkout heading / options", "#content h1, #content legend", first=True)