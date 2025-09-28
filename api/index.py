import json
import numpy as np
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

# Enable CORS globally
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def load_telemetry_data():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(os.path.dirname(current_dir), 'q-vercel-latency.json')
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [{"region": "apac", "service": "analytics", "latency_ms": 204.41, "uptime_pct": 98.045, "timestamp": 20250301}]

telemetry_data = load_telemetry_data()

class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.get("/")
async def health_check(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return {"message": "The health check is successful!"}

@app.options("/{path:path}")
async def preflight(path: str, response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return {"message": "CORS preflight OK"}

@app.post("/")
@app.post("/telemetry")
async def process_telemetry(request: TelemetryRequest, response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    try:
        result = {}
        for region in request.regions:
            region_data = [record for record in telemetry_data if record["region"] == region]
            if not region_data:
                result[region] = {"avg_latency": 0.0, "p95_latency": 0.0, "avg_uptime": 0.0, "breaches": 0}
                continue

            latencies = [record["latency_ms"] for record in region_data]
            uptimes = [record["uptime_pct"] for record in region_data]

            avg_latency = np.mean(latencies)
            p95_latency = np.percentile(latencies, 95)
            avg_uptime = np.mean(uptimes)
            breaches = sum(1 for latency in latencies if latency > request.threshold_ms)

            result[region] = {
                "avg_latency": round(avg_latency, 2),
                "p95_latency": round(p95_latency, 2),
                "avg_uptime": round(avg_uptime, 3),
                "breaches": breaches
            }

        return {"regions": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
