import dataclasses
from typing import List

from src.domain.month_status import MonthStatus
from src.domain.payment import Payment


@dataclasses.dataclass
class MonthlyExpenditure:
    month_status: MonthStatus
    payments: List[Payment]


@dataclasses.dataclass
class CreditHistory:
    expenditure: List[MonthlyExpenditure]
