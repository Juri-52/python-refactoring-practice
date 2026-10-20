from dataclasses import dataclass


@dataclass
class Book:
    title: str
    daily_late_fee: int
