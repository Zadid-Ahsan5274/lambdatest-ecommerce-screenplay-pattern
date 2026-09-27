from __future__ import annotations

import platform
import sys
from importlib.metadata import version
from pathlib import Path

import allure
import pytest
from playwright.sync_api import sync_playwright

from config.settings import ALLURE_RESULTS_DIR, ARTIFACTS_DIR, settings
from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.actor import Actor
from screenplay.ensure import Ensure
from screenplay.tasks.authentication import Register
from screenplay.ui.account_pages import RegisterPage
from utils.allure_helpers import attach_page_source, attach_screenshot, write_environment_properties
from utils.data_factory import build_user
from utils.helpers import safe_name
from utils.logger import get_logger

log = get_logger("tests")


# ------------------------------------------------------------------ CLI / hooks
def pytest_addoption(parser):
    parser.addoption("--browser-name", choices=["chromium", "firefox", "webkit"], help="Browser to run")
    parser.addoption("--headed", action="store_true", help="Run with a visible browser")


def pytest_configure(config):
    browser = config.getoption("--browser-name")
    if browser:
        settings.browser = browser
    if config.getoption("--headed"):
        settings.headless = False


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())


def pytest_sessionfinish(session):
    if hasattr(session.config, "workerinput"):  # only the xdist controller writes it
        return
    results_dir = getattr(session.config.option, "allure_report_dir", None) or ALLURE_RESULTS_DIR
    write_environment_properties(
        results_dir,
        {
            "Browser": settings.browser,
            "Base URL": settings.base_url,
            "Headless": settings.headless,
            "Python": sys.version.split()[0],
            "Playwright": version("playwright"),
            "Platform": platform.platform(),
        },
    )


def _failed(request) -> bool:
    return any(
        getattr(request.node, attr, None) is not None and getattr(request.node, attr).failed
        for attr in ("rep_setup", "rep_call")
    )


# ------------------------------------------------------------------ fixtures
@pytest.fixture(autouse=True)
def _allure_metadata():
    allure.dynamic.parameter("browser", settings.browser)
    allure.dynamic.tag(settings.browser)


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="session")
def browser(playwright_instance):
    launcher = getattr(playwright_instance, settings.browser)
    instance = launcher.launch(headless=settings.headless, slow_mo=settings.slow_mo)
    log.info("Launched %s (headless=%s)", settings.browser, settings.headless)
    yield instance
    instance.close()


@pytest.fixture
def context(browser, request):
    kwargs = dict(
        viewport={"width": settings.viewport_width, "height": settings.viewport_height},
        locale=settings.locale,
        ignore_https_errors=True,
    )
    if settings.video != "off":
        kwargs["record_video_dir"] = str(ARTIFACTS_DIR / "videos")
    ctx = browser.new_context(**kwargs)
    ctx.set_default_timeout(settings.default_timeout)
    ctx.set_default_navigation_timeout(settings.navigation_timeout)
    tracing = settings.trace != "off"
    if tracing:
        ctx.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield ctx

    failed = _failed(request)
    name = safe_name(request.node.nodeid)
    if tracing:
        if settings.trace == "on" or failed:
            trace_path = ARTIFACTS_DIR / "traces" / f"{name}.zip"
            trace_path.parent.mkdir(parents=True, exist_ok=True)
            ctx.tracing.stop(path=str(trace_path))
            allure.attach.file(str(trace_path), name="playwright-trace", extension="zip")
        else:
            ctx.tracing.stop()

    videos = [p.video for p in ctx.pages if p.video]
    ctx.close()
    for video in videos:
        try:
            path = Path(video.path())
        except Exception:
            continue
        if settings.video == "on" or failed:
            allure.attach.file(str(path), name="video", attachment_type=allure.attachment_type.WEBM)
        else:
            path.unlink(missing_ok=True)


@pytest.fixture
def page(context, request):
    pg = context.new_page()
    yield pg
    if _failed(request) or settings.screenshot == "on":
        attach_screenshot(pg, "screenshot")
    if _failed(request):
        allure.attach(pg.url, name="final-url", attachment_type=allure.attachment_type.TEXT)
        attach_page_source(pg)


@pytest.fixture
def actor(page):
    shopper = Actor.named("Sam").can(BrowseTheWeb.using(page))
    yield shopper
    shopper.wrap_up()


@pytest.fixture
def registered_actor(actor):
    """An actor who has just registered a brand-new account (and is therefore logged in)."""
    user = build_user()
    actor.remember("user", user)
    actor.attempts_to(
        Register.as_new_customer(user),
        Ensure.that(RegisterPage.SUCCESS_HEADING).contains_text("Your Account Has Been Created"),
    )
    return actor