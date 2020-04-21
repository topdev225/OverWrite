from dataclasses import dataclass
from flask import request
import json


@dataclass
class Filter:
    name: str
    table: str
    separator: str
    field: str
    op: str

    variants: str = None
    model: str = None

    @property
    def value(self):
        settings = request.headers.get("R-Settings")
        settings = json.loads(settings)
        filters = settings["filters"]
        filter_name = f"{self.table}{self.separator}{self.field}"
        return filters.get(filter_name)
