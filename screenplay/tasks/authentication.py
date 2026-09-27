from __future__ import annotations

from config.routes import Routes
from screenplay.core.interfaces import Task
from screenplay.interactions import Check, Click, Enter, Open
from screenplay.ui.account_pages import LoginPage, RegisterPage
from utils.data_factory import User


class Register(Task):
    def __init__(self, user: User) -> None:
        self._user = user
        self._accept_privacy = True

    @classmethod
    def as_new_customer(cls, user: User) -> "Register":
        return cls(user)

    def without_accepting_privacy_policy(self) -> "Register":
        self._accept_privacy = False
        return self

    def __str__(self) -> str:
        return f"registers a new account for {self._user.email}"

    def perform_as(self, actor) -> None:
        u = self._user
        actor.attempts_to(
            Open.route(Routes.REGISTER),
            Enter.text(u.first_name).into(RegisterPage.FIRST_NAME),
            Enter.text(u.last_name).into(RegisterPage.LAST_NAME),
            Enter.text(u.email).into(RegisterPage.EMAIL),
            Enter.text(u.telephone).into(RegisterPage.TELEPHONE),
            Enter.text(u.password).into(RegisterPage.PASSWORD),
            Enter.text(u.confirm_password).into(RegisterPage.CONFIRM_PASSWORD),
        )
        if self._accept_privacy:
            actor.attempts_to(Check.the(RegisterPage.PRIVACY_POLICY))
        actor.attempts_to(Click.on(RegisterPage.CONTINUE))


class Login(Task):
    def __init__(self, email: str, password: str) -> None:
        self._email = email
        self._password = password

    @classmethod
    def with_credentials(cls, email: str, password: str) -> "Login":
        return cls(email, password)

    @classmethod
    def as_(cls, user: User) -> "Login":
        return cls(user.email, user.password)

    def __str__(self) -> str:
        return f"logs in as {self._email}"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Open.route(Routes.LOGIN),
            Enter.text(self._email).into(LoginPage.EMAIL),
            Enter.text(self._password).into(LoginPage.PASSWORD),
            Click.on(LoginPage.LOGIN_BUTTON),
        )


class Logout(Task):
    @classmethod
    def now(cls) -> "Logout":
        return cls()

    def __str__(self) -> str:
        return "logs out"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Open.route(Routes.LOGOUT))