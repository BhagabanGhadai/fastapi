from repositories.user import UserRepository
from models.user import User
from sqlalchemy.orm import Session

class UserService:
    def __init__(self,db:Session):
        self.repository=UserRepository(db)

    def create_user(self,user_data:dict)->User:
        try:
            user_exist = self.repository.get_by_username(user_data["username"])
            if user_exist is not None:
                raise ValueError("User already exists")

            return self.repository.create_user(user_data)
        except Exception as e:
            raise e

    def get_user_by_username(self,username:str)->User:
        try:
            user= self.repository.get_by_username(username)
            if user is None:
                raise ValueError("User not found")
            return user
        except Exception as e:
            raise e
        
    def get_user_by_id(self,id:int)->User:
        try:
            user=self.repository.get_by_id(id)
            if user is None:
                raise ValueError("User not found")
            return user
        except Exception as e:
            raise e

    def get_all_users(self)->list[User]:
        try:
            return self.repository.get_all_users()
        except Exception as e:
            raise e

    def update_user(self,user_id:int,user_data:dict)->User:
        try:
            updated_user = self.repository.update_user(user_id, user_data)
            if updated_user is None:
                raise ValueError("User not found")
            return updated_user
        except Exception as e:
            raise e

    def delete_user(self,user_id:int)->User:
        try:
            deleted_user = self.repository.delete_user(user_id)
            if deleted_user is None:
                raise ValueError("User not found")
            return deleted_user
        except Exception as e:
            raise e    