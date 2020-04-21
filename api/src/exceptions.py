class OrderWriteException(Exception):
    pass


class LoginRequired(OrderWriteException):
    pass


class RoleException(OrderWriteException):
    pass


class ValidationError(OrderWriteException):
    status_code = 400
