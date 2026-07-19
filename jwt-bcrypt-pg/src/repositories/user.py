from models.user import User
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self,db:Session):
        self.db=db

    def create_user(self,user_data:dict)->User:
        db_user=User(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_by_username(self,username:str)->User|None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self,user_id:int)->User|None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_all_users(self)->list[User]:
        return self.db.query(User).all()

    def update_user(self,user_id:int,user_data:dict)->User|None:
        db_user=self.get_by_id(user_id)
        if db_user is None:
            return None
        
        username = user_data.get("username")
        if username is not None:
            db_user.username = username

        password = user_data.get("password")
        if password is not None:
            db_user.password = password

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self,user_id:int)->User|None:
        db_user=self.get_by_id(user_id)
        if db_user is None:
            return None
        self.db.delete(db_user)
        self.db.commit()
        return db_user