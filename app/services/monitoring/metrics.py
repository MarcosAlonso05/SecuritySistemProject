from prometheus_client import Counter, Histogram

EVENT_COUNTER = Counter(
    "events_processed_total",
    "Cantidad total de eventos procesados por sensor",
    ["sensor_type"]
)

EVENT_LATENCY = Histogram(
    "event_processing_latency_seconds",
    "Latencia del procesamiento de eventos en segundos",
    ["sensor_type"]
)
