from __future__ import annotations

from playwright.sync_api import Page

from screenplay.core.interfaces import Ability


class BrowseTheWeb(Ability):
    def __init__(self, page: Page) -> None:
        self._page = page

    @classmethod
    def using(cls, page: Page) -> "BrowseTheWeb":
        return cls(page)

    @property
    def page(self) -> Page:
        return self._page


def current_page(actor) -> Page:
    return actor.ability_to(BrowseTheWeb).page