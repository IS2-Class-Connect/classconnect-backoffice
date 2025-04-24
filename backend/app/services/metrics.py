# app/metrics.py

from prometheus_client import Counter

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total de peticiones recibidas"
)
