from dataclasses import dataclass


@dataclass
class Sort:
    name: str
    field: str
    direction: int
