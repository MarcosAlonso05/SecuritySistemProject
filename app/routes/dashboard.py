# app/routes/dashboard.py  (añadir o modificar)
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.routes.auth import SESSIONS
from app.services.store import get_all_last_events, get_all_stats
from app.dependencies import require_role

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard")
def dashboard_html(request: Request, user=Depends(require_role("operator"))):
    token = request.cookies.get("session_token")
    if not token or token not in SESSIONS:
        return RedirectResponse("/login")
    events = get_all_last_events(limit_per_sensor=20)
    stats = get_all_stats()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "events": events,
        "stats": stats,
        "user": SESSIONS[token]
    })

@router.get("/dashboard/metrics")
def metrics_page(request: Request, user=Depends(require_role("viewer"))):
    stats = get_all_stats()
    return templates.TemplateResponse("metrics.html", {
        "request": request,
        "stats": stats
    })