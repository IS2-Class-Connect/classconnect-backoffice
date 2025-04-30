from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from app.databases.mongo import MongoDB
from app.services.admin import AdminService
from app.controllers.admin import AdminController
from app.routers.admin import AdminRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    DB_URI = os.getenv("DB_URI")
    if not DB_URI:
        raise ValueError("No database URI was provided")

    DB_NAME = os.getenv("DB_NAME")
    if not DB_NAME:
        raise ValueError("No database name was provided")

    try:
        db = MongoDB(DB_URI, DB_NAME)
    except:
        raise RuntimeError("coudn't connect to db")

    service = AdminService(db)
    controller = AdminController(service)
    admin_router = AdminRouter(controller)
    app.include_router(admin_router.router)

    yield

    db.close()


app = FastAPI(lifespan=lifespan)
