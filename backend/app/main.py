from fastapi import FastAPI
import os

from app.database.db import AdminDB
from app.services.admin import AdminService
from app.controllers.admin import Controller
from app.routers.admin import AdminRouter

app = FastAPI()

# Global shared dependencies
db: AdminDB | None = None

@app.on_event("startup")
async def on_startup():
    global db
    db = AdminDB(os.environ["MONGO_URI"], os.environ["DB_NAME"])
    service = AdminService(db)
    controller = Controller(service)
    admin_router = AdminRouter(controller)
    app.include_router(admin_router.router)

@app.on_event("shutdown")
async def on_shutdown():
    global db
    if db:
        db.close()

