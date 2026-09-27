from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

ARTIFACTS_DIR = ROOT_DIR / "artifacts"
ALLURE_RESULTS_DIR = ROOT_DIR / "allure-results"

def _bool(name: str, default: bool) -> bool:
    return os.getenv(name,str(default)).strip().lower() in {"1","true","yes","on"}
 
def _int(name: str, default: int) -> int:
    return int(os.getenv(name,default))


@dataclass
class Settings:
    base_url:str = "https://ecommerce-playground.lambdatest.io/"
    headless:bool = True
    browser:str = "chromium"
    slow_mo:int = 0
    viewport_width:int = 1440
    viewport_height:int = 900
    default_timeout: int = 20_000        # was 15_000
    navigation_timeout: int = 45_000      # was 30_000
    expect_timeout: int = 12_000          # was 10_000
    trace:str = "retain-on-failure"
    video:str = "retain-on-failure"
    screenshot:str = "only-on-failure"
    locale:str = "en-US"
    default_password:str = "123456"

    @classmethod
    def from_env(cls) -> "Settings":
        d = cls()
        return cls(
            base_url = os.getenv("BASE_URL",d.base_url).rstrip("/"),
            browser = os.getenv("BROWSER",d.browser).lower(),
            headless = _bool("HEADLESS",d.headless),
            slow_mo = _int("SLOW_MO",d.slow_mo),
            viewport_width = _int("VIEWPORT_WIDTH",d.viewport_width),
            viewport_height = _int("VIEWPORT_HEIGHT",d.viewport_height),
            default_timeout = _int("DEFAULT_TIMEOUT",d.default_timeout),
            navigation_timeout = _int("NAVIGATION_TIMEOUT",d.navigation_timeout),
            expect_timeout = _int("EXPECT_TIMEOUT",d.expect_timeout),
            trace = os.getenv("TRACE",d.trace).lower(),
            video = os.getenv("VIDEO",d.video).lower(),
            screenshot = os.getenv("SCREENSHOT",d.screenshot).lower(),
            default_password = os.getenv("DEFAULT_PASSWORD",d.default_password).lower(),
        )
settings = Settings.from_env()