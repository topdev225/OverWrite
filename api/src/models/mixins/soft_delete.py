from safrs import DB as db

from src.exceptions import ValidationError


# FIXME: is this used anywhere? the API won't ever trigger this, and we might want it to.
class SoftDeleteMixin(object):
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    def delete(self, *args, **kwargs):
        id = kwargs.get(self.object_id, None)

        if not id:
            raise ValidationError("Invalid resource identifier specified")

        instance = self.SAFRSObject.get_instance(id)

        if kwargs.get("soft", False):
            instance.is_deleted = True
            db.session.add(instance)
        else:
            db.session.delete(instance)
