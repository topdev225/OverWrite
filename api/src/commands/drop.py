from safrs import DB as db


def drop():
    db.reflect()
    db.drop_all()
    print("Drop finished")
