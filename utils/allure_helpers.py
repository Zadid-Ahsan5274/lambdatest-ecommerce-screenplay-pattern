from __future__ import annotations

from pathlib import Path

import allure
from playwright.sync_api import Page

from utils.logger import get_logger

log = get_logger("allure")


def attach_text(name: str, body: str) -> None:
    allure.attach(body, name=name, attachment_type=allure.attachment_type.TEXT)


def attach_screenshot(page: Page, name: str = "screenshot") -> None:
    try:
        allure.attach(
            page.screenshot(full_page=True),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:  # page may already be closed
        log.warning("Could not capture screenshot: %s", exc)


def attach_page_source(page: Page) -> None:
    try:
        allure.attach(page.content(), name="page-source", attachment_type=allure.attachment_type.HTML)
    except Exception as exc:
        log.warning("Could not capture page source: %s", exc)


def write_environment_properties(directory: str | Path, props: dict) -> None:
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    lines = [f"{k.replace(' ', '_')}={v}" for k, v in props.items()]
    (directory / "environment.properties").write_text("\n".join(lines), encoding="utf-8")