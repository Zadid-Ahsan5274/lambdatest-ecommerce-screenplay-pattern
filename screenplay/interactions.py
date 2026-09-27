from __future__ import annotations

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from config.routes import url_for
from screenplay.abilities.browse_the_web import current_page
from screenplay.core.interfaces import Interaction
from screenplay.ui.target import Target
from utils.helpers import retry
from utils.logger import get_logger

log = get_logger("interactions")
_RESPONSE_TIMEOUT = 8_000


class Open(Interaction):
    def __init__(self, url: str) -> None:
        self._url = url

    @classmethod
    def route(cls, route: str, **params) -> "Open":
        return cls(url_for(route, **params))

    @classmethod
    def url(cls, url: str) -> "Open":
        return cls(url)

    def __str__(self) -> str:
        return f"opens {self._url}"

    def perform_as(self, actor) -> None:
        page = current_page(actor)

        def _go(wait_until: str):
            page.goto(self._url, wait_until=wait_until)

        try:
            retry(lambda: _go("domcontentloaded"), attempts=2, delay=1.5, exceptions=(PlaywrightTimeoutError,))
        except PlaywrightTimeoutError:
            log.warning("domcontentloaded timed out for %s, retrying with 'load'", self._url)
            _go("load")


class Click(Interaction):
    def __init__(self, target: Target) -> None:
        self._target = target
        self._keywords: tuple = ()

    @classmethod
    def on(cls, target: Target) -> "Click":
        return cls(target)

    def and_wait_for_response_from(self, *url_keywords: str) -> "Click":
        """Wait for an XHR/navigation response whose URL contains all keywords."""
        self._keywords = url_keywords
        return self

    def __str__(self) -> str:
        return f"clicks on {self._target}"

    def perform_as(self, actor) -> None:
        page = current_page(actor)
        locator = self._target.resolve_for(actor)
        if not self._keywords:
            locator.click()
            return
        clicked = False
        try:
            with page.expect_response(
                lambda r: all(k in r.url for k in self._keywords), timeout=_RESPONSE_TIMEOUT
            ):
                locator.click()
                clicked = True
        except PlaywrightTimeoutError:
            if not clicked:
                raise
            log.warning("No response matching %s after clicking %s", self._keywords, self._target)


class Enter(Interaction):
    def __init__(self, text: str) -> None:
        self._text = text
        self._target: Target | None = None

    @classmethod
    def text(cls, value: str) -> "Enter":
        return cls(value)

    def into(self, target: Target) -> "Enter":
        self._target = target
        return self

    def __str__(self) -> str:
        secret = any(w in str(self._target).lower() for w in ("password", "confirm"))
        shown = "******" if secret else self._text
        return f"enters '{shown}' into {self._target}"

    def perform_as(self, actor) -> None:
        self._target.resolve_for(actor).fill(self._text)


class Press(Interaction):
    def __init__(self, key: str) -> None:
        self._key = key
        self._target: Target | None = None

    @classmethod
    def key(cls, key: str) -> "Press":
        return cls(key)

    def on(self, target: Target) -> "Press":
        self._target = target
        return self

    def __str__(self) -> str:
        return f"presses {self._key} on {self._target}"

    def perform_as(self, actor) -> None:
        self._target.resolve_for(actor).press(self._key)


class Check(Interaction):
    """Ticks a (possibly custom-styled) checkbox."""

    def __init__(self, target: Target) -> None:
        self._target = target

    @classmethod
    def the(cls, target: Target) -> "Check":
        return cls(target)

    def __str__(self) -> str:
        return f"ticks {self._target}"

    def perform_as(self, actor) -> None:
        self._target.resolve_for(actor).check(force=True)


class SelectOption(Interaction):
    def __init__(self, label: str) -> None:
        self._label = label
        self._target: Target | None = None
        self._reload = False

    @classmethod
    def labelled(cls, label: str) -> "SelectOption":
        return cls(label)

    def from_(self, target: Target) -> "SelectOption":
        self._target = target
        return self

    def and_wait_for_page_reload(self) -> "SelectOption":
        self._reload = True
        return self

    def __str__(self) -> str:
        return f"selects '{self._label}' from {self._target}"

    def perform_as(self, actor) -> None:
        locator = self._target.resolve_for(actor)
        if self._reload:
            with current_page(actor).expect_navigation():
                locator.select_option(label=self._label)
        else:
            locator.select_option(label=self._label)