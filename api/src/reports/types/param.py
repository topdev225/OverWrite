from dataclasses import dataclass
from flask import request


@dataclass
class Param:
    name: str
    type_: str
    meta: dict

    def extract(self):
        return request.args.get(self.name)
