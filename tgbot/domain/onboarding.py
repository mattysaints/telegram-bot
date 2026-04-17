from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class MenuAction:
    key: str
    label: str
    url: Optional[str] = None


@dataclass(frozen=True)
class StartScreen:
    text: str
    actions: List[MenuAction]


@dataclass(frozen=True)
class UserSnapshot:
    user_id: int
    first_name: str
    is_new: bool

