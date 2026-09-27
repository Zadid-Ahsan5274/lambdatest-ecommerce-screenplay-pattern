from __future__ import annotations
import uuid
from dataclasses import dataclass
from typing import Optional
from faker import Faker
from config.settings import settings

_fake = Faker()

@dataclass
class User:
    first_name:str
    last_name:str
    email:str
    telephone:str
    password:str
    confirm_password:Optional[str] = None

    def __post_init__(self) -> None:
        if self.confirm_password is None:
            self.confirm_password = self.password

def unique_email(prefix:str="qa")->str:
    return f"{prefix}.{uuid.uuid4().hex[:12]}@example.com"

def build_user(**overrides) -> User:
    data = dict(
        first_name=_fake.first_name()[:30],
        last_name=_fake.last_name()[:30],
        email=unique_email(),
        telephone=_fake.numerify("##########"),
        password=settings.default_password,
    )
    data.update(overrides)
    return User(**data)


