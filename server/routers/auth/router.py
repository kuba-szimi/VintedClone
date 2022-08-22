from fastapi import APIRouter, HTTPException, Query, Form
from fastapi_utils.cbv import cbv
from typing import List, Optional

router = APIRouter()


@router.post("/auth/login/")
def login(username: str = Form(), password: str = Form()):
    return {"username": username}
