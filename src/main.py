# from contextlib import asynccontextmanager

from fastapi import FastAPI

from src import api
from src.config import config
from src.database import db

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     try:
#         await db.connect()
#         yield
#     finally:
#         await db.disconnect()


def init_app():
    app = FastAPI()

    @app.on_event("startup")
    def startup():
        db.connect(config.DATABASE_URL)

    @app.on_event("shutdown")
    async def shutdown():
        await db.disconnect()

    app.include_router(
        api.router,
        prefix="/api",
    )

    return app


app = init_app()

# app = FastAPI(lifespan=lifespan)
