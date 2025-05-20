import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, order=True, slots=True)
class TR:
    time: datetime
    data: str
    id: uuid.UUID
    s_id: uuid.UUID
    _groups: list[str] = field(init=False, repr=False)
    _nerrors: int = field(init=False, repr=True)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_groups", self.data.split(" "))
        object.__setattr__(self, "_nerrors", self.data.count("_"))

    def __len__(self) -> int:
        return len(self.data)

    def __str__(self) -> str:
        return f"[ {self.data} ]"

    @property
    def groups(self) -> list[str]:
        return self._groups

    @property
    def nerrors(self) -> int:
        return self._nerrors
