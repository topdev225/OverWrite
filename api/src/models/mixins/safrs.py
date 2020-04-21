from safrs import DB as db, SAFRSBase


class SAFRSMixin(SAFRSBase):
    # by overloading __init__, we get rid of the point in SAFRS where models are added to the
    # session and committed. by specifying this, the `_create_instance` method in SAFRS will pick
    # up the slack and do the session add/commit
    db_commit = False

    def __init__(self, *args, **kwargs):
        """Bypass SAFRSBase.__init__ and just run SQLAlchemy's initializer.

        Notes
        -----
        SAFRS tries to do some validation in its initializer, but it pretty much just causes issues
        with validators not running correctly or at the right time. They validators are pretty much
        worthless as well.
        """
        db.Model.__init__(self, *args, **kwargs)

    @classmethod
    def _s_sample(cls):
        """Override SAFRS method to stop trying to get the first instance of a model.

        Notes
        -----
        The original method in SAFRS calls `cls.query.first()` in order to get some example fields
        to put in the swagger documentation. It is totally unnecessary and it breaks the SQL session
        if there are no models in the table.
        """
        return None
