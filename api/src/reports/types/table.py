from abc import ABC, abstractmethod
from typing import List, Tuple
from sqlalchemy_filters import apply_filters as sqla_filters

from src.plugins import logger


class Table(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def params(self) -> List[object]:
        pass

    @property
    @abstractmethod
    def filters(self) -> List[object]:
        pass

    @property
    @abstractmethod
    def sortings(self) -> List[object]:
        pass

    def apply_filters(self, query):
        # Main arguments for filter_by statement
        filter_spec = []
        # Iterate filters to build spec
        for filter_ in self.filters:
            if filter_.value:
                filter_spec.append(
                    {
                        "model": filter_.model,
                        "field": filter_.field,
                        "op": filter_.op,
                        "value": filter_.value,
                    }
                )
        # Apply spec
        logger.info(filter_spec)
        query = sqla_filters(query, filter_spec)
        # Return
        return query

    def apply_sort(self, query):
        return query

    def format_price(self, val: float) -> str:
        return "${:.2f}".format(val)

    @abstractmethod
    def generate(self, *args, **kwargs) -> Tuple[List[str], List[dict], List[dict]]:
        """
        Method for generating table data
        Returns 3 values:
            - list of columns(str)
            - list of rows(dict)
            - list of meta(dict)
        """
        pass
