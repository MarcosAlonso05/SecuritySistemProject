from typing import Dict
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

USERS_DB: Dict[str, Dict] = {}

def get_user(username: str):
    return USERS_DB.get(username)

def create_user(username: str, password: str, role: str = "viewer"):
    if not isinstance(password, str):
        password = str(password)
    hashed = pwd_context.hash(password)
    USERS_DB[username] = {"username": username, "hashed_password": hashed, "role": role}
    return USERS_DB[username]

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
