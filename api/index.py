import json
import numpy as np
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()

    def do_POST(self):
        try:
            # Load telemetry data
            with open('q-vercel-latency.json', 'r') as f:
                telemetry = json.load(f)
            
            # Read request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data.decode('utf-8'))
            
            regions = body.get("regions", [])
            threshold = body.get("threshold_ms", 180)

            results = {}
            for region in regions:
                records = [r for r in telemetry if r["region"] == region]
                if not records:
                    continue

                latencies = [r["latency_ms"] for r in records]
                uptimes = [r["uptime_pct"] for r in records]

                avg_latency = float(np.mean(latencies))
                p95_latency = float(np.percentile(latencies, 95))
                avg_uptime = float(np.mean(uptimes))
                breaches = sum(1 for l in latencies if l > threshold)

                results[region] = {
                    "avg_latency": avg_latency,
                    "p95_latency": p95_latency,
                    "avg_uptime": avg_uptime,
                    "breaches": breaches
                }

            # Send response with comprehensive CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            self.end_headers()
            
            response = json.dumps(results)
            self.wfile.write(response.encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS, GET')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            self.end_headers()
            
            error_response = json.dumps({'error': str(e)})
            self.wfile.write(error_response.encode('utf-8'))
