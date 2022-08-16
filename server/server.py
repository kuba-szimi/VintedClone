from fastapi import FastAPI
from server.routers import router as main_board_router

#app = FastAPI(dependencies=[Depends(get_query_token)])
app = FastAPI()
app.include_router(main_board_router)
