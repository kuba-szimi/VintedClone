from typing import List, Dict
from fastapi import HTTPException
from passlib.hash import bcrypt
from server.db_models.users.users_model import UserModel
from server.database import get_db
from server.schemas.users_schema import UserCreate, User


class UserManager:

    def __init__(self):
        self._db = next(get_db())

    def retrieve_users(self) -> List[User]:
        return self._db.query(UserModel).all()

    def retrieve_users_by_id(self, user_id: int) -> User:
        db_user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User Not Found")
        return db_user

    @staticmethod
    def hash_password(plain_password: str):
        return bcrypt.hash(plain_password)

    def retrieve_users_by_username(self, username: str) -> User:
        return self._db.query(UserModel).filter(UserModel.username == username).first()

    def create_user(self, user: UserCreate):
        hashed_password = self.hash_password(user.password)
        db_user = UserModel(
            email=user.email,
            hashed_password=hashed_password,
            username=user.username,
            disabled=False,
            location=user.location
        )
        self._db.add(db_user)
        self._db.commit()
        self._db.refresh(db_user)
        return db_user

    def update_item_description(self, user_id: int, bio: str) -> User:
        user_to_be_updated = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        if user_to_be_updated is None:
            raise HTTPException(status_code=404, detail="User Not Found")
        user_to_be_updated.bio = bio
        self._db.add(user_to_be_updated)
        self._db.commit()
        self._db.refresh(user_to_be_updated)
        return user_to_be_updated

    def delete_user(self, user_id: int) -> str:
        db_user = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User Not Found")
        self._db.query(UserModel).filter(UserModel.id == user_id).delete(synchronize_session=False)
        self._db.commit()
        return "User has been deleted successfully"



