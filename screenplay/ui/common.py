from screenplay.ui.target import Target


class Common:
    CONTENT = Target("Main content area", "#content")
    SEARCH_INPUT = Target("Header search box", "input[name='search']:visible", first=True)
    PRODUCT_CARDS = Target("Product cards", ".product-thumb")
    PRODUCT_NAMES = Target("Product names", ".product-thumb h4 a")
    PRODUCT_PRICES = Target("Product prices", ".product-thumb .price-new")
    PRODUCT_LINK = Target("Product link '{name}'", ".product-thumb h4 a:text-is('{name}')", first=True)
    ERROR_MESSAGE = Target("Error message", ".alert-danger, #notification-box-top .toast-body", first=True)
    SUCCESS_TOAST = Target("Success toast", "#notification-box-top .toast-body", first=True)
    # was ".text-danger" only — this theme doesn't always tag inline validation text that way
    FIELD_ERRORS = Target("Field validation errors", ".text-danger, .invalid-feedback, .form-text.text-danger")