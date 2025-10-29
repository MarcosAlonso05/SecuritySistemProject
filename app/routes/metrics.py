from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth import SESSIONS
from prometheus_client import REGISTRY
from app.services.store import get_all_stats

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/metrics")
def show_metrics(request: Request):
    token = request.cookies.get("session_token")
    if not token or token not in SESSIONS:
        return RedirectResponse("/login")

    user = SESSIONS[token]

    stats = {}
    for metric in REGISTRY.collect():
        if metric.name == "events_processed_total":
            for sample in metric.samples:
                sensor = sample.labels.get("sensor_type", "unknown")
                stats.setdefault(sensor, {"count": 0, "latencies": []})
                stats[sensor]["count"] += int(sample.value)
        elif metric.name == "event_processing_latency_seconds":
            for sample in metric.samples:
                sensor = sample.labels.get("sensor_type", "unknown")
                stats.setdefault(sensor, {"count": 0, "latencies": []})
                if sample.name.endswith("_sum"):
                    stats[sensor]["latencies"].append(float(sample.value))

    computed_prometheus = {}
    for s, st in stats.items():
        latencies = st["latencies"]
        if not latencies:
            computed_prometheus[s] = {
                "count": st["count"],
                "avg_latency": 0,
                "median_latency": 0,
                "max_latency": 0
            }
            continue

        latencies.sort()
        total_sum = sum(latencies)
        total_count = st["count"]
        
        avg_latency = total_sum / total_count if total_count > 0 else 0
        
        simple_count = len(latencies)
        avg_latency_original = sum(latencies) / simple_count if simple_count > 0 else 0
        median_latency = latencies[simple_count // 2] if simple_count > 0 else 0
        max_latency = max(latencies) if simple_count > 0 else 0


        computed_prometheus[s] = {
            "count": st["count"],
            "avg_latency": avg_latency_original,
            "median_latency": median_latency,
            "max_latency": max_latency
        }

    dashboard_stats = get_all_stats()

    return templates.TemplateResponse("metrics.html", {
        "request": request,
        "user": user,
        "stats_prometheus": computed_prometheus,
        "stats_dashboard": dashboard_stats
    })
