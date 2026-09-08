import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="msg-worker-queue", description="AS Cloud Live Messaging Queue Worker & Notification Dispatcher", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

START_TIME = time.time()

@app.get("/")
def root():
    return {
        "service": "msg-worker-queue",
        "status": "online",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "cluster": "AS-Cloud-Messages",
        "restart_cycle": "5h-managed"
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "msg-worker-queue", "timestamp": time.time()}
