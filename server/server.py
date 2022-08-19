from fastapi import FastAPI
from .routers.main_board.router import router as main_board_router
from server.database import Base, engine

#Base.metadata.create_all(bind=engine)

#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
app.include_router(main_board_router)
