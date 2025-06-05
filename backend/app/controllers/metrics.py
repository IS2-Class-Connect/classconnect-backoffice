from fastapi import APIRouter
from fastapi.responses import Response
from prometheus_client import (
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    PlatformCollector,
    ProcessCollector,
    Gauge,
    Counter,
    Histogram,
)
import threading
import logging
import psutil
import os

registry = CollectorRegistry()
PlatformCollector(registry=registry)
ProcessCollector(registry=registry)

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


class MetricsController:
    def __init__(self):
        self.router = APIRouter(prefix="/admins", tags=["admins"])
        threading.Thread(target=track_usage, daemon=True).start()

    def get_metrics(self):
        logging.info("Trying to get metrics")
        return Response(
            content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST
        )
