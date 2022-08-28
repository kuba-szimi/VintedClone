import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Union, Dict
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from server.database import get_db
from server.db_models.users.users_model import UserModel

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# def fake_hash_password(password: str):
#     return password + "notreallyhashed"


# async def get_current_user(token: str = Depends(oauth2_scheme)) -> LoginUser:
#     auth_user = AuthUser()
#     user = auth_user.fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


def authenticate_user(username: str, password: str):
    auth_user = AuthUser()
    user = auth_user.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    auth_user = AuthUser()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as jwte:
        print(jwte)
        raise credentials_exception
    user = auth_user.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: LoginUser = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def login_for_access_token(username: str, password: str) -> str:
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return access_token


# async def get_login_user(username: str, password: str) -> str:
#     auth_user = AuthUser()
#     db_user = auth_user.get_user(username)
#     if not db_user:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     hashed_password = fake_hash_password(password)
#     if not hashed_password == db_user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     return db_user.username
