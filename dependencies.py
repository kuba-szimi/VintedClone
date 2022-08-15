from fastapi import Header, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()


async def get_token_header(x_token: str = Header()):
    if x_token != os.getenv("SEC_TOKEN"):
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def get_query_token(token: str):
    if token != os.getenv("QUERY_TOKEN"):
        raise HTTPException(status_code=400, detail="No Jessica token provided")
