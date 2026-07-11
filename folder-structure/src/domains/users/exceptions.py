from src.core.exceptions import Conflict, NotFound


class UserNotFound(NotFound):
    detail = "User not found"


class EmailAlreadyRegistered(Conflict):
    detail = "Email already registered"
