from __future__ import annotations

from typing import List

from screenplay.abilities.browse_the_web import current_page
from screenplay.core.interfaces import Question
from screenplay.ui.target import Target
from utils.helpers import parse_price


class Text(Question[str]):
    def __init__(self, target: Target) -> None:
        self._target = target

    @classmethod
    def of(cls, target: Target) -> "Text":
        return cls(target)

    def answered_by(self, actor) -> str:
        return (self._target.resolve_for(actor).text_content() or "").strip()


class Texts(Question[List[str]]):
    def __init__(self, target: Target) -> None:
        self._target = target

    @classmethod
    def of(cls, target: Target) -> "Texts":
        return cls(target)

    def answered_by(self, actor) -> List[str]:
        return [t.strip() for t in self._target.resolve_for(actor).all_inner_texts()]


class Prices(Question[List[float]]):
    def __init__(self, target: Target) -> None:
        self._target = target

    @classmethod
    def of(cls, target: Target) -> "Prices":
        return cls(target)

    def answered_by(self, actor) -> List[float]:
        return [parse_price(t) for t in self._target.resolve_for(actor).all_inner_texts()]


class Value(Question[str]):
    def __init__(self, target: Target) -> None:
        self._target = target

    @classmethod
    def of(cls, target: Target) -> "Value":
        return cls(target)

    def answered_by(self, actor) -> str:
        return self._target.resolve_for(actor).input_value()


class NumberOf(Question[int]):
    def __init__(self, target: Target) -> None:
        self._target = target

    @classmethod
    def elements(cls, target: Target) -> "NumberOf":
        return cls(target)

    def answered_by(self, actor) -> int:
        return self._target.resolve_for(actor).count()


class CurrentUrl(Question[str]):
    def answered_by(self, actor) -> str:
        return current_page(actor).url