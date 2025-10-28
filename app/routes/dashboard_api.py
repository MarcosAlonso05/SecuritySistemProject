from fastapi import APIRouter, Depends
from app.services.store import get_all_last_events, get_all_stats
from app.dependencies import require_role

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/operator")
def operator_dashboard_api(user=Depends(require_role("operator"))):
    events = get_all_last_events(limit_per_sensor=20)
    stats = get_all_stats()
    return {"events": events, "stats": stats}
