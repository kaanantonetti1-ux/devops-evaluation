import os
import time

from flask import Flask, Response, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from redis import Redis
from redis.exceptions import RedisError

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", "6379"))
app_version = os.getenv("APP_VERSION", "local")

redis_client = Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True,
)

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["endpoint", "code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["route"],
)

APP_INFO = Gauge(
    "app_deployed_version",
    "Currently deployed application version",
    ["version"],
)

APP_INFO.labels(version=app_version).set(1)


@app.before_request
def start_timer():
    request.start_time = time.perf_counter()


@app.after_request
def record_metrics(response):
    route = request.url_rule.rule if request.url_rule else request.path

    duration = time.perf_counter() - request.start_time

    REQUEST_COUNT.labels(
        endpoint=route,
        code=str(response.status_code),
    ).inc()

    REQUEST_LATENCY.labels(
        route=route,
    ).observe(duration)

    return response


@app.get("/")
def index():
    return jsonify(
        {
            "message": "DevOps Evaluation API",
            "status": "running",
        }
    ), 200


@app.get("/health")
def health():
    try:
        redis_client.ping()

        return jsonify(
            {
                "status": "healthy",
                "redis": "connected",
            }
        ), 200

    except RedisError:
        return jsonify(
            {
                "status": "unhealthy",
                "redis": "disconnected",
            }
        ), 503


@app.get("/counter")
def counter():
    try:
        value = redis_client.incr("request_counter")

        return jsonify(
            {
                "counter": value,
            }
        ), 200

    except RedisError:
        return jsonify(
            {
                "error": "Redis unavailable",
            }
        ), 503


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST,
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )