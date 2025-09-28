import json
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# This is the correct way to structure your app for Vercel
app = FastAPI()

# Add the CORS middleware to your app
# This will handle all preflight OPTIONS requests and add the required headers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- IMPORTANT ---
# Paste the content of your q-vercel-latency.json file here.
# Reading from a file will not work on Vercel.
telemetry_data = [
    {
        "region": "apac",
        "service": "payments",
        "latency_ms": 144.12,
        "uptime_pct": 99.373,
        "timestamp": 20250301
    },
    {
        "region": "apac",
        "service": "catalog",
        "latency_ms": 136.83,
        "uptime_pct": 97.355,
        "timestamp": 20250302
    },
    {
        "region": "apac",
        "service": "recommendations",
        "latency_ms": 141.16,
        "uptime_pct": 99.445,
        "timestamp": 20250303
    },
    {
        "region": "apac",
        "service": "catalog",
        "latency_ms": 163.51,
        "uptime_pct": 97.916,
        "timestamp": 20250304
    },
    {
        "region": "apac",
        "service": "analytics",
        "latency_ms": 153.33,
        "uptime_pct": 98.106,
        "timestamp": 20250305
    },
    {
        "region": "apac",
        "service": "analytics",
        "latency_ms": 163.78,
        "uptime_pct": 97.2,
        "timestamp": 20250306
    },
    {
        "region": "apac",
        "service": "support",
        "latency_ms": 165.62,
        "uptime_pct": 99.182,
        "timestamp": 20250307
    },
    {
        "region": "apac",
        "service": "catalog",
        "latency_ms": 192.44,
        "uptime_pct": 99.43,
        "timestamp": 20250308
    },
    {
        "region": "apac",
        "service": "support",
        "latency_ms": 144.59,
        "uptime_pct": 98.004,
        "timestamp": 20250309
    },
    {
        "region": "apac",
        "service": "checkout",
        "latency_ms": 189.57,
        "uptime_pct": 98.855,
        "timestamp": 20250310
    },
    {
        "region": "apac",
        "service": "support",
        "latency_ms": 169.46,
        "uptime_pct": 97.734,
        "timestamp": 20250311
    },
    {
        "region": "apac",
        "service": "recommendations",
        "latency_ms": 167.15,
        "uptime_pct": 97.105,
        "timestamp": 20250312
    },
    {
        "region": "emea",
        "service": "recommendations",
        "latency_ms": 156.68,
        "uptime_pct": 99.342,
        "timestamp": 20250301
    },
    {
        "region": "emea",
        "service": "recommendations",
        "latency_ms": 130.62,
        "uptime_pct": 97.191,
        "timestamp": 20250302
    },
    {
        "region": "emea",
        "service": "recommendations",
        "latency_ms": 182.38,
        "uptime_pct": 97.592,
        "timestamp": 20250303
    },
    {
        "region": "emea",
        "service": "checkout",
        "latency_ms": 134.89,
        "uptime_pct": 98.402,
        "timestamp": 20250304
    },
    {
        "region": "emea",
        "service": "recommendations",
        "latency_ms": 226.81,
        "uptime_pct": 99.095,
        "timestamp": 20250305
    },
    {
        "region": "emea",
        "service": "analytics",
        "latency_ms": 206.56,
        "uptime_pct": 99.33,
        "timestamp": 20250306
    },
    {
        "region": "emea",
        "service": "payments",
        "latency_ms": 105.92,
        "uptime_pct": 99.449,
        "timestamp": 20250307
    },
    {
        "region": "emea",
        "service": "catalog",
        "latency_ms": 199.41,
        "uptime_pct": 97.164,
        "timestamp": 20250308
    },
    {
        "region": "emea",
        "service": "recommendations",
        "latency_ms": 208.52,
        "uptime_pct": 99.067,
        "timestamp": 20250309
    },
    {
        "region": "emea",
        "service": "catalog",
        "latency_ms": 181.4,
        "uptime_pct": 98.825,
        "timestamp": 20250310
    },
    {
        "region": "emea",
        "service": "support",
        "latency_ms": 140.34,
        "uptime_pct": 98.118,
        "timestamp": 20250311
    },
    {
        "region": "emea",
        "service": "recommendations",
        "latency_ms": 203.71,
        "uptime_pct": 99.482,
        "timestamp": 20250312
    },
    {
        "region": "amer",
        "service": "payments",
        "latency_ms": 130.18,
        "uptime_pct": 98.447,
        "timestamp": 20250301
    },
    {
        "region": "amer",
        "service": "analytics",
        "latency_ms": 147.05,
        "uptime_pct": 97.822,
        "timestamp": 20250302
    },
    {
        "region": "amer",
        "service": "catalog",
        "latency_ms": 210.61,
        "uptime_pct": 98.056,
        "timestamp": 20250303
    },
    {
        "region": "amer",
        "service": "recommendations",
        "latency_ms": 204.77,
        "uptime_pct": 97.263,
        "timestamp": 20250304
    },
    {
        "region": "amer",
        "service": "checkout",
        "latency_ms": 173.95,
        "uptime_pct": 98.475,
        "timestamp": 20250305
    },
    {
        "region": "amer",
        "service": "checkout",
        "latency_ms": 207.91,
        "uptime_pct": 97.703,
        "timestamp": 20250306
    },
    {
        "region": "amer",
        "service": "support",
        "latency_ms": 114.85,
        "uptime_pct": 97.384,
        "timestamp": 20250307
    },
    {
        "region": "amer",
        "service": "payments",
        "latency_ms": 135.68,
        "uptime_pct": 98.727,
        "timestamp": 20250308
    },
    {
        "region": "amer",
        "service": "analytics",
        "latency_ms": 176.31,
        "uptime_pct": 97.921,
        "timestamp": 20250309
    },
    {
        "region": "amer",
        "service": "analytics",
        "latency_ms": 111.92,
        "uptime_pct": 98.993,
        "timestamp": 20250310
    },
    {
        "region": "amer",
        "service": "checkout",
        "latency_ms": 155.93,
        "uptime_pct": 97.46,
        "timestamp": 20250311
    },
    {
        "region": "amer",
        "service": "recommendations",
        "latency_ms": 216.55,
        "uptime_pct": 98.258,
        "timestamp": 20250312
    }
    ]


class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

# The assignment doesn't require a health check endpoint, but it's good practice.
# Vercel will route GET requests to "/" here.
@app.get("/")
async def health_check():
    return {"status": "API is running"}

# Vercel will route POST requests to "/" or "/telemetry" here.
@app.post("/api/index") # Main endpoint as per vercel routing
@app.post("/")
@app.post("/telemetry")
async def process_telemetry(request: TelemetryRequest):
    result = {}
    for region in request.regions:
        region_data = [d for d in telemetry_data if d["region"] == region]
        if not region_data:
            result[region] = {"avg_latency": 0.0, "p95_latency": 0.0, "avg_uptime": 0.0, "breaches": 0}
            continue

        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]
        
        breaches = sum(1 for latency in latencies if latency > request.threshold_ms)

        result[region] = {
            "avg_latency": round(np.mean(latencies), 2),
            "p95_latency": round(np.percentile(latencies, 95), 2),
            "avg_uptime": round(np.mean(uptimes), 3),
            "breaches": breaches,
        }

    return {"regions": result}