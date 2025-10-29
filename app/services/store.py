# app/services/store.py
from typing import Dict, Any
from collections import defaultdict, deque
import statistics

MAX_EVENTS_PER_SENSOR = 100

LAST_EVENTS: Dict[str, deque] = defaultdict(lambda: deque(maxlen=MAX_EVENTS_PER_SENSOR))

STATS: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
    "count": 0,
    "latencies": []
})

def add_event(sensor_type: str, event: Dict[str, Any], latency: float | None = None) -> None:
    LAST_EVENTS[sensor_type].appendleft(event)
    STATS[sensor_type]["count"] += 1
    if latency is not None:
        STATS[sensor_type]["latencies"].append(latency)

def get_last_events(sensor_type: str, limit: int = 20):
    return list(LAST_EVENTS.get(sensor_type, []))[:limit]

def get_all_last_events(limit_per_sensor: int = 20):
    return {s: list(deque_obj)[:limit_per_sensor] for s, deque_obj in LAST_EVENTS.items()}

def get_stats(sensor_type: str):
    s = STATS.get(sensor_type, {"count": 0, "latencies": []})
    latencies = s["latencies"]
    avg = statistics.mean(latencies) if latencies else 0.0
    median = statistics.median(latencies) if latencies else 0.0
    maximum = max(latencies) if latencies else 0.0
    return {
        "count": s["count"],
        "avg_latency": avg,
        "median_latency": median,
        "max_latency": maximum,
        "samples": len(latencies)
    }

def get_all_stats():
    return {s: get_stats(s) for s in STATS.keys()}
