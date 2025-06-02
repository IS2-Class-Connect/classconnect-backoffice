from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.databases.mongo import MongoDB
from app.services.admin import AdminService
from app.controllers.admin import AdminController
from app.routers.admin import AdminRouter, registry
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
)
import psutil
import threading
import logging
import os
import time

# Prometheus Initialization
CPU_USAGE = Gauge(
    "cpu_usage_percent",
    "CPU usage percentage",
    registry=registry,
)
MEMORY_USAGE = Gauge(
    "memory_usage_bytes",
    "Memory usage in bytes",
    registry=registry,
)
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"],
    registry=registry,
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    registry=registry,
)


# Resource usage tracking
def track_usage():
    process = psutil.Process(os.getpid())
    while True:
        CPU_USAGE.set(process.cpu_percent(interval=5.0))
        MEMORY_USAGE.set(process.memory_info().rss)


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
        raise ValueError("No gateway token was provided")

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
    threading.Thread(target=track_usage, daemon=True).start()

    yield

    db.close()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Update metrics
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(
        process_time,
    )

    return response


# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
