from __future__ import annotations
from dataclasses import dataclass

class BudgetExceeded(RuntimeError):
    pass

@dataclass(frozen=True)
class BudgetPolicy:
    soft_limit: float
    hard_limit: float

    def __post_init__(self) -> None:
        if self.soft_limit < 0 or self.hard_limit <= 0:
            raise ValueError("Budget limits must be positive")
        if self.soft_limit > self.hard_limit:
            raise ValueError("Soft limit cannot exceed hard limit")

@dataclass
class BudgetLedger:
    policy: BudgetPolicy
    committed: float = 0.0
    reserved: float = 0.0

    def reserve(self, amount: float) -> str:
        if amount < 0:
            raise ValueError("Reservation cannot be negative")
        projected = self.committed + self.reserved + amount
        if projected > self.policy.hard_limit:
            raise BudgetExceeded(
                f"Projected spend {projected:.2f} exceeds hard limit {self.policy.hard_limit:.2f}"
            )
        self.reserved += amount
        return "soft_limit_warning" if projected > self.policy.soft_limit else "ok"

    def commit(self, amount: float) -> None:
        if amount < 0 or amount > self.reserved:
            raise ValueError("Commit must be between zero and reserved amount")
        self.reserved -= amount
        self.committed += amount
