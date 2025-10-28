from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.dependencies import require_role 
from app.routes.auth import SESSIONS

router = APIRouter(
    prefix="/simulator",
    tags=["simulator"],
    dependencies=[Depends(require_role("admin"))]
)

templates = Jinja2Templates(directory="app/templates")

@router.get("", response_class=HTMLResponse)
async def get_simulator_panel(request: Request):
    
    return templates.TemplateResponse("simulate.html", {"request": request})
