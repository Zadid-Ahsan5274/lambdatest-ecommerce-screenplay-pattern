from __future__ import annotations

from playwright.sync_api import Locator

from screenplay.abilities.browse_the_web import current_page


class Target:
    """A named locator. Use {placeholders} + .of(**kw) for dynamic targets."""

    def __init__(self, description: str, selector: str, first: bool = False) -> None:
        self.description = description
        self.selector = selector
        self.first = first

    def of(self, **kwargs) -> "Target":
        return Target(self.description.format(**kwargs), self.selector.format(**kwargs), self.first)

    def resolve_for(self, actor) -> Locator:
        locator = current_page(actor).locator(self.selector)
        return locator.first if self.first else locator

    def __str__(self) -> str:
        return self.description