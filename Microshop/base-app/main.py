from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # For fast test of work with DB
    # async with db_helper.engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all/drop_all)
    yield
    # shutdowm
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router, prefix=settings.api.prefix)


@main_app.get("/")
async def root():
    return {"message": "Hello World"}


@main_app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run('main:main_app', host=settings.run.host, port=settings.run.port, reload=True)
