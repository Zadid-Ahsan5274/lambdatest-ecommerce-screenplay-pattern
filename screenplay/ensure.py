from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

from playwright.sync_api import expect

from config.settings import settings
from screenplay.abilities.browse_the_web import current_page
from screenplay.core.interfaces import Interaction
from screenplay.ui.target import Target

if TYPE_CHECKING:
    from screenplay.core.actor import Actor


def _t() -> int:
    return settings.expect_timeout


class Ensure(Interaction):
    """Auto-waiting assertions expressed as Performables (backed by playwright.expect)."""

    def __init__(self, description: str, check: Callable[["Actor"], None]) -> None:
        self._description = description
        self._check = check

    def __str__(self) -> str:
        return f"ensures {self._description}"

    def perform_as(self, actor) -> None:
        self._check(actor)

    @staticmethod
    def that(target: Target) -> "_TargetAssertions":
        return _TargetAssertions(target)

    @staticmethod
    def the_page() -> "_PageAssertions":
        return _PageAssertions()


class _TargetAssertions:
    def __init__(self, target: Target) -> None:
        self._target = target

    def _make(self, text: str, fn: Callable) -> Ensure:
        return Ensure(f"{self._target} {text}", fn)

    def is_visible(self) -> Ensure:
        return self._make("is visible", lambda a: expect(self._target.resolve_for(a)).to_be_visible(timeout=_t()))

    def is_present(self) -> Ensure:
        """At least one matching element is visible."""
        return self._make(
            "is present",
            lambda a: expect(self._target.resolve_for(a).first).to_be_visible(timeout=_t()),
        )

    def is_not_visible(self) -> Ensure:
        return self._make("is not visible", lambda a: expect(self._target.resolve_for(a)).to_be_hidden(timeout=_t()))

    def has_text(self, text: str) -> Ensure:
        return self._make(f"has text '{text}'", lambda a: expect(self._target.resolve_for(a)).to_have_text(text, timeout=_t()))

    def contains_text(self, text: str) -> Ensure:
        return self._make(
            f"contains text '{text}'",
            lambda a: expect(self._target.resolve_for(a)).to_contain_text(text, timeout=_t()),
        )

    def has_value(self, value: str) -> Ensure:
        return self._make(f"has value '{value}'", lambda a: expect(self._target.resolve_for(a)).to_have_value(value, timeout=_t()))

    def has_count(self, count: int) -> Ensure:
        return self._make(f"has {count} element(s)", lambda a: expect(self._target.resolve_for(a)).to_have_count(count, timeout=_t()))

    def has_element_with_text(self, text: str) -> Ensure:
        return self._make(
            f"has an element containing '{text}'",
            lambda a: expect(self._target.resolve_for(a).filter(has_text=text).first).to_be_visible(timeout=_t()),
        )


class _PageAssertions:
    def has_url_containing(self, fragment: str) -> Ensure:
        pattern = re.compile(f".*{re.escape(fragment)}.*")
        return Ensure(
            f"the URL contains '{fragment}'",
            lambda a: expect(current_page(a)).to_have_url(pattern, timeout=_t()),
        )

    def has_title_containing(self, fragment: str) -> Ensure:
        pattern = re.compile(f".*{re.escape(fragment)}.*")
        return Ensure(
            f"the page title contains '{fragment}'",
            lambda a: expect(current_page(a)).to_have_title(pattern, timeout=_t()),
        )