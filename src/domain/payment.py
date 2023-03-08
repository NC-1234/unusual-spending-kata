import dataclasses
from enum import Enum

class Category(Enum):
    ENTERTAINMENT = "entertainment"
    RESTAURANTS = "restaurants"
    GOLF = "golf"
    GROCERIES = "groceries"
    TRAVEL = "travel"

@dataclasses.dataclass
class Payment:
    price: float
    description: str
    category: Category