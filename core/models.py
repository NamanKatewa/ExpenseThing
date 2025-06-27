from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class Expense:
    id: int
    description: str
    amount: float
    paid_by: str
    involved_people: List[str]
    split_amount_per_person: float
    date: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)


@dataclass
class Payment:
    id: int
    payer: str
    payee: str
    amount: float
    date: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    description: str = "Direct Payment"

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)
