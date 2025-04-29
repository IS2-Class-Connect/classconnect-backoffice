from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
from app.databases.dict import DictDB
from app.services.admin import AdminService
from app.controllers.admin import Controller
from app.routers.admin import AdminRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    DB_URI = os.getenv("DB_URI", "")
    DB_NAME = os.getenv("DB_NAME", "")

    # db = AdminDB(DB_URI, DB_NAME)
    db = DictDB("", "")
    service = AdminService(db)
    controller = Controller(service)
    admin_router = AdminRouter(controller)
    app.include_router(admin_router.router)

    yield

    db.close()


app = FastAPI(lifespan=lifespan)
