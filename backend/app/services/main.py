# app/main.py

from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest

from app.metrics import REQUEST_COUNT


app = FastAPI()

@app.get("/")
def home():
    REQUEST_COUNT.inc()
    return {"message": "API online 👋"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
