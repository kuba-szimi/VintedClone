from typing import List, Optional
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from server.auth.auth_user import LoginUser, authenticate_user, get_current_active_user


router = APIRouter()


@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": form_data.username, "token_type": "bearer"}


@router.post("/auth/login/")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = await authenticate_user(form_data.username, form_data.password)
    return {"access_token": username, "token_type": "bearer"}


@router.get("/users/me", response_model=LoginUser)
async def read_users_me(current_user: LoginUser = Depends(get_current_active_user)):
    return await get_current_active_user(current_user)
