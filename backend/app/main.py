from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

    ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
    if not ADMIN_TOKEN:
        raise ValueError("No admin token was provided")

    GATEWAY_URL = os.getenv("GATEWAY_URL")
    if not GATEWAY_URL:
        raise ValueError("No gateway URL was provided")

    try:
        db = MongoDB(DB_URI, DB_NAME)
    except:
        raise RuntimeError("couldn't connect to db")

    service = AdminService(db, ADMIN_TOKEN, GATEWAY_URL)
    controller = AdminController(service)
    admin_router = AdminRouter(controller)
    app.include_router(admin_router.router)

    yield

    db.close()


app = FastAPI(lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
