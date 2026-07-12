from sqlalchemy.orm import Session
from repositorie.user import UserRepository
from models.user import User

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.repository.get_by_username(username)

    def create_user(self, user_data: dict) -> User:
        return self.repository.create(user_data)
