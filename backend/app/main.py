from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
from app.databases.dict import DictDB
from app.services.admin import AdminService
from app.controllers.admin import AdminController
from app.routers.admin import AdminRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    DB_URI = os.getenv("DB_URI", "")
    DB_NAME = os.getenv("DB_NAME", "")

    try:
        # db = AdminDB(DB_URI, DB_NAME)
        db = DictDB(DB_URI, DB_NAME)
    except:
        raise RuntimeError("coudn't connect to db")

    service = AdminService(db)
    controller = AdminController(service)
    admin_router = AdminRouter(controller)
    app.include_router(admin_router.router)

    yield

    db.close()


app = FastAPI(lifespan=lifespan)
