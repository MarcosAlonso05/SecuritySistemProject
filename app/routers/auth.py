from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserCreate, UserOut, Token
from app.models.user import create_user, get_user, verify_password
from app.utils.authentication import create_access_token
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    created = create_user(user.username, user.password, user.role)
    return {"username": created["username"], "role": created["role"]}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas")
    token_data = {"sub": user["username"], "role": user["role"]}
    access_token = create_access_token(token_data, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token}
