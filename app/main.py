from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.routes import auth, home, sensors, dashboard, metrics, simulate
from app.routes.auth import SESSIONS

app = FastAPI(title="Security Monitoring System", docs_url=None, redoc_url=None)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(sensors.router)
app.include_router(dashboard.router)
app.include_router(metrics.router)
app.include_router(simulate.router)

@app.get("/docs", response_class=HTMLResponse)
async def custom_docs(request: Request):
    token = request.cookies.get("session_token")
    if not token or token not in SESSIONS:
        return RedirectResponse("/login")
    
    user = SESSIONS[token]

    if user["role"] != "admin":
        return HTMLResponse("<h2>Acceso denegado: solo el administrador puede ver la documentación.</h2>", status_code=403)

    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentación del Sistema")