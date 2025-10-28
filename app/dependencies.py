from fastapi import Request
from fastapi.responses import RedirectResponse
from app.routes.auth import SESSIONS

def require_role(min_role: str):
    
    role_order = {"viewer": 1, "operator": 2, "admin": 3}

    def dependency(request: Request):
        token = request.cookies.get("session_token")
        user = SESSIONS.get(token)

        if not user:
            return RedirectResponse("/login")

        user_role = user["role"]
        if role_order[user_role] < role_order[min_role]:
            return RedirectResponse("/dashboard")

        return user

    return dependency