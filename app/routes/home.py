from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.routes.auth import SESSIONS

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/home")
def home(request: Request):
    token = request.cookies.get("session_token")
    if not token or token not in SESSIONS:
        return RedirectResponse("/login")

    user = SESSIONS[token]
    role = user["role"]

    return templates.TemplateResponse("home.html", {
        "request": request,
        "username": user["username"],
        "role": role
    })
