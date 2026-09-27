from __future__ import annotations

from typing import Optional

from config.routes import Routes
from screenplay.core.interfaces import Task
from screenplay.interactions import Click, Enter, Open
from screenplay.ui.account_pages import EditAccountPage, PasswordPage
from screenplay.ui.shop_pages import ContactPage


class UpdateProfile(Task):
    def __init__(self, first_name: str) -> None:
        self._first_name = first_name

    @classmethod
    def first_name(cls, first_name: str) -> "UpdateProfile":
        return cls(first_name)

    def __str__(self) -> str:
        return f"changes the first name to '{self._first_name}'"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Open.route(Routes.EDIT_ACCOUNT),
            Enter.text(self._first_name).into(EditAccountPage.FIRST_NAME),
            Click.on(EditAccountPage.CONTINUE).and_wait_for_response_from("account/edit"),
        )


class ChangePassword(Task):
    def __init__(self, new_password: str, confirmation: Optional[str] = None) -> None:
        self._new = new_password
        self._confirm = confirmation if confirmation is not None else new_password

    @classmethod
    def to(cls, new_password: str, confirmation: Optional[str] = None) -> "ChangePassword":
        return cls(new_password, confirmation)

    def __str__(self) -> str:
        return "changes the account password"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Open.route(Routes.PASSWORD),
            Enter.text(self._new).into(PasswordPage.PASSWORD),
            Enter.text(self._confirm).into(PasswordPage.CONFIRM),
            Click.on(PasswordPage.CONTINUE).and_wait_for_response_from("account/password"),
        )


class SubmitContactForm(Task):
    def __init__(self, name: str, email: str, enquiry: str) -> None:
        self._name, self._email, self._enquiry = name, email, enquiry

    @classmethod
    def with_details(cls, name: str, email: str, enquiry: str) -> "SubmitContactForm":
        return cls(name, email, enquiry)

    def __str__(self) -> str:
        return f"submits the contact form as {self._email}"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Open.route(Routes.CONTACT),
            Enter.text(self._name).into(ContactPage.NAME),
            Enter.text(self._email).into(ContactPage.EMAIL),
            Enter.text(self._enquiry).into(ContactPage.ENQUIRY),
            Click.on(ContactPage.SUBMIT),
        )