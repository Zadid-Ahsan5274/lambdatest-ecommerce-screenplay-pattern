from __future__ import annotations

from typing import Any, Dict, Type, TypeVar

import allure

from screenplay.core.interfaces import Ability, Performable, Question

A = TypeVar("A", bound=Ability)
T = TypeVar("T")


class AbilityMissing(Exception):
    pass


class Actor:
    def __init__(self, name: str) -> None:
        self.name = name
        self._abilities: Dict[type, Ability] = {}
        self._memory: Dict[str, Any] = {}

    @classmethod
    def named(cls, name: str) -> "Actor":
        return cls(name)

    def can(self, *abilities: Ability) -> "Actor":
        for ability in abilities:
            self._abilities[type(ability)] = ability
        return self

    def ability_to(self, ability_type: Type[A]) -> A:
        try:
            return self._abilities[ability_type]  # type: ignore[return-value]
        except KeyError:
            raise AbilityMissing(f"{self.name} cannot {ability_type.__name__}") from None

    def attempts_to(self, *performables: Performable) -> None:
        for performable in performables:
            with allure.step(f"{self.name} {performable}"):
                performable.perform_as(self)

    def should(self, *assertions: Performable) -> None:
        self.attempts_to(*assertions)

    def asks_for(self, question: Question[T]) -> T:
        return question.answered_by(self)

    def remember(self, key: str, value: Any) -> None:
        self._memory[key] = value

    def recall(self, key: str) -> Any:
        return self._memory[key]

    def wrap_up(self) -> None:
        for ability in self._abilities.values():
            ability.tear_down()