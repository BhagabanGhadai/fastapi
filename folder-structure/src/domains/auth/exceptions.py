from src.core.exceptions import Unauthorized


class InvalidCredentials(Unauthorized):
    detail = "Invalid email or password"


class InvalidToken(Unauthorized):
    detail = "Invalid or expired token"
