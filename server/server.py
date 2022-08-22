from fastapi import FastAPI, Depends
from .routers.auth.router import router as auth_router
from .routers.items_management.router import router as items_router
from .routers.users_management.router import router as users_router
from .routers.main_board.router import router as main_board_router
from .dependencies import get_query_token, get_token_header
from server.database import Base, engine
from server.internal import admin

#Base.metadata.create_all(bind=engine)

#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
app.include_router(auth_router, tags=["auth"])
app.include_router(items_router, tags=["items"])
app.include_router(users_router, tags=["users"])
app.include_router(main_board_router, tags=["main board"])
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
