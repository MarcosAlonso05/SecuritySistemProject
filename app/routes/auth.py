from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

SESSIONS = {}

# Base de usuarios inicial
USERS = {
    "admin": {"password": "1234", "role": "admin"},
    "operator": {"password": "1234", "role": "operator"},
    "viewer": {"password": "1234", "role": "viewer"},
}

# -------------------------
# LOGIN
# -------------------------
@router.get("/")
def root():
    return RedirectResponse("/login")

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = USERS.get(username)
    if not user or user["password"] != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales incorrectas"})
    token = f"token_{username}"
    SESSIONS[token] = {"username": username, "role": user["role"]}
    response = RedirectResponse("/home", status_code=302)
    response.set_cookie("session_token", token)
    return response

@router.get("/logout")
def logout(request: Request):
    token = request.cookies.get("session_token")
    if token and token in SESSIONS:
        del SESSIONS[token]
    response = RedirectResponse("/login", status_code=302)
    response.delete_cookie("session_token")
    return response


# -------------------------
# REGISTER
# -------------------------
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_user(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    if username in USERS:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "El usuario ya existe"
        })
    
    USERS[username] = {"password": password, "role": role}
    token = f"token_{username}"
    SESSIONS[token] = {"username": username, "role": role}

    response = RedirectResponse("/home", status_code=302)
    response.set_cookie("session_token", token)
    return response
