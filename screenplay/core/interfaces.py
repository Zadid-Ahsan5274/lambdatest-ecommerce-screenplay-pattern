from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from screenplay.core.actor import Actor

T = TypeVar("T")


class Ability(ABC):
    """Something an Actor is able to do (e.g. browse the web)."""

    def tear_down(self) -> None:
        pass


class Performable(ABC):
    @abstractmethod
    def perform_as(self, actor: "Actor") -> None: ...

    def __str__(self) -> str:  # used as the Allure step name
        return re.sub(r"(?<!^)(?=[A-Z])", " ", type(self).__name__).lower()


class Task(Performable):
    """Business-level goal composed of other performables."""


class Interaction(Performable):
    """Low-level UI action or assertion."""


class Question(ABC, Generic[T]):
    @abstractmethod
    def answered_by(self, actor: "Actor") -> T: ...