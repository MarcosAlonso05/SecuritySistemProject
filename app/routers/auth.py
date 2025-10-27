from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, UserOut, Token
from app.models.user import create_user, get_user, verify_password
from app.utils.authentication import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth")

@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    new_user = create_user(user.username, user.password, user.role)
    return {"username": new_user["username"], "role": new_user["role"]}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}