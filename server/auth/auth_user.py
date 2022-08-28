from typing import Union, Dict
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from pydantic import BaseModel
from server.database import get_db
from server.db_models.users.users_model import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginUser(BaseModel):
    username: str
    email: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(LoginUser):
    hashed_password: str


class AuthUser:

    def __init__(self):
        self.db = next(get_db())

    def get_user(self, username: str) -> UserInDB:
        user = self.db.query(
            UserModel.username, UserModel.email, UserModel.hashed_password, UserModel.disabled)\
            .filter(UserModel.username == username)\
            .first()
        return user

    def fake_decode_token(self, token: str) -> UserInDB:
        # This doesn't provide any security at all
        # Check the next version
        user = self.get_user(token)
        return user


def fake_hash_password(password: str):
    return password + "notreallyhashed"


async def get_current_user(token: str = Depends(oauth2_scheme)) -> LoginUser:
    auth_user = AuthUser()
    user = auth_user.fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: LoginUser = Depends(get_current_user)) -> LoginUser:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def authenticate_user(username: str, password: str) -> str:
    auth_user = AuthUser()
    db_user = auth_user.get_user(username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = fake_hash_password(password)
    if not hashed_password == db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return db_user.username
