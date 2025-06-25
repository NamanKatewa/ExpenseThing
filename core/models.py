from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class Expense:
    id: int
    description: str
    amount: float
    paid_by: str  # Name of the person who paid
    involved_people: List[str]  # Names of people who are splitting the expense
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
    payer: str  # Person who made the payment
    payee: str  # Person who received the payment
    amount: float
    date: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    description: str = "Direct Payment"  # Optional description for clarity

    def to_dict(self) -> Dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)
