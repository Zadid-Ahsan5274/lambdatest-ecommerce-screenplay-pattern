from screenplay.ui.target import Target


class RegisterPage:
    FIRST_NAME = Target("First name field", "#input-firstname")
    LAST_NAME = Target("Last name field", "#input-lastname")
    EMAIL = Target("E-Mail field", "#input-email")
    TELEPHONE = Target("Telephone field", "#input-telephone")
    PASSWORD = Target("Password field", "#input-password")
    CONFIRM_PASSWORD = Target("Password confirm field", "#input-confirm")
    PRIVACY_POLICY = Target("Privacy policy checkbox", "input[name='agree']")
    CONTINUE = Target("Continue button", "input[value='Continue']", first=True)
    SUCCESS_HEADING = Target("Registration heading", "#content h1", first=True)


class LoginPage:
    EMAIL = Target("Login E-Mail field", "#input-email")
    PASSWORD = Target("Login Password field", "#input-password")
    LOGIN_BUTTON = Target("Login button", "input[value='Login']", first=True)


class AccountPage:
    CONTAINER = Target("My Account page", "#account-account")


class EditAccountPage:
    FIRST_NAME = Target("First name field", "#input-firstname")
    CONTINUE = Target("Continue button", "input[value='Continue']", first=True)


class PasswordPage:
    PASSWORD = Target("New Password field", "#input-password")
    CONFIRM = Target("Password confirm field", "#input-confirm")
    CONTINUE = Target("Continue button", "input[value='Continue']", first=True)