import re
import time
from typing import Callable, TypeVar

T = TypeVar("T")


def parse_price(text: str) -> float:
    match = re.search(r"\d[\d,]*\.?\d*", text)
    if not match:
        raise ValueError(f"No price found in: {text!r}")
    return float(match.group().replace(",", ""))


def safe_name(value: str, max_len: int = 150) -> str:
    return re.sub(r"[^\w\-.]+", "_", value)[:max_len]


def retry(fn: Callable[[], T], attempts: int = 2, delay: float = 1.0, exceptions=(Exception,)) -> T:
    """Retry a flaky call. Re-raises the last exception if all attempts fail."""
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except exceptions as exc:  # noqa: PERF203
            last_exc = exc
            if attempt < attempts:
                time.sleep(delay)
    raise last_exc  # type: ignore[misc]