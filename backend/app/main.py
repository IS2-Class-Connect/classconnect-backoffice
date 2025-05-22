from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.databases.mongo import MongoDB
from app.services.admin import AdminService
from app.controllers.admin import AdminController
from app.routers.admin import AdminRouter
import logging


def initialize_log(logging_level):
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            record.levelname = f"{record.levelname}:".ljust(9)
            return super().format(record)

    handler = logging.StreamHandler()
    handler.setFormatter(
        CustomFormatter(
            fmt="%(levelname)s %(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    )

    logging.basicConfig(level=logging_level, handlers=[handler])


@asynccontextmanager
async def lifespan(app: FastAPI):

    DB_URI = os.getenv("DB_URI")
    if not DB_URI:
        raise ValueError("No database URI was provided")

    DB_NAME = os.getenv("DB_NAME")
    if not DB_NAME:
        raise ValueError("No database name was provided")

    GATEWAY_TOKEN = os.getenv("GATEWAY_TOKEN")
    if not GATEWAY_TOKEN:
        raise ValueError("No admin token was provided")

    GATEWAY_URL = os.getenv("GATEWAY_URL")
    if not GATEWAY_URL:
        raise ValueError("No gateway URL was provided")

    try:
        db = MongoDB(DB_URI, DB_NAME)
    except:
        raise RuntimeError("couldn't connect to db")

    service = AdminService(db, GATEWAY_TOKEN, GATEWAY_URL)
    controller = AdminController(service)
    admin_router = AdminRouter(controller)
    app.include_router(admin_router.router)
    initialize_log(logging.INFO)

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
