from typing import Any
from json import JSONEncoder, dumps as default_dumps
from dataclasses import is_dataclass, asdict
from decimal import Decimal
from datetime import date
from enum import Enum


class EnhancedJSONEncoder(JSONEncoder):
    def default(self, value):
        if is_dataclass(value):
            return asdict(value)
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, Enum):
            return value.name
        return super().default(value)


def dumps(value: Any)-> str:
    return default_dumps(value, cls=EnhancedJSONEncoder)
