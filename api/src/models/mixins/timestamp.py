from safrs import DB as db
from sqlalchemy.sql import func


class TimestampMixin(object):
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    modified_at = db.Column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )
