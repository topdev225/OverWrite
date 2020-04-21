from safrs import DB as db


class UpdateMixin(object):
    def update(self, args):
        """Update attributes of a SQLAlchemy model using ORM.

        Parameters
        ----------
        args : `dict`
            Where keys are model attributes and values are, well, values.

        Returns
        -------
        `None`
        """
        db.session.query(self.__class__).filter(self.__class__.id == self.id).update(args)
