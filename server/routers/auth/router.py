from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from server.auth.auth_user import LoginUser, login_for_access_token, get_current_active_user, Token


router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = await login_for_access_token(form_data.username, form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=LoginUser)
async def read_users_me(current_user: LoginUser = Depends(get_current_active_user)):
    return await get_current_active_user(current_user)


@router.get("/users/me/items/")
async def read_own_items(current_user: LoginUser = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]