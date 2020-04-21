import hashlib
from uuid import uuid4

from conf import conf


def hash_password(password):
    return hashlib.sha256((password + str(conf.SECRET)).encode("utf-8")).hexdigest()


def random_username():
    return uuid4().hex


def random_password():
    return hash_password(uuid4().hex)
