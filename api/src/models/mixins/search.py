import json

from src import models


class SearchMixin(object):
    @classmethod
    def _s_filter(cls, args):
        """Search fields on the model using custom SAFRS filter.

        This is an adapter that will work with the filtering syntax already in the frontend. Here is
        an example of the type of JSON this is expecting:

            [{
                "field": "username",
                "op": "ilike",
                "value": "foobar"
            },
                "field": "name",
                "model": "Distributor",
                "op": "ilike",
                "value": "foobar"
            ]}

        Parameters
        ----------
        args : `str`
            A JSON serialized dictionary where keys are fields and a value is text to search.

        Returns
        -------
        `BaseQuery`
        """
        args = json.loads(args)

        query = cls.query

        for term in args:
            if term.get("model"):
                model_obj = getattr(models, term["model"])
                query = query.join(model_obj)
                obj = getattr(model_obj, term["field"])
            else:
                obj = getattr(cls, term["field"])

            if term.get("op") == "ilike":
                query = query.filter(obj.ilike(f"%{term['value']}%"))
            elif term.get("op") == "==":
                query = query.filter(obj == term["value"])
            elif term.get("op") == "!=":
                query = query.filter(obj != term["value"])
            elif term.get("op") == ">":
                query = query.filter(obj > term["value"])
            elif term.get("op") == ">=":
                query = query.filter(obj >= term["value"])
            elif term.get("op") == "<":
                query = query.filter(obj < term["value"])
            elif term.get("op") == "<=":
                query = query.filter(obj <= term["value"])
            else:
                raise NotImplementedError

        return query
