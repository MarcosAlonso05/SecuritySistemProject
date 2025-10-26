from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "viewer"

class UserOut(BaseModel):
    username: str
    role: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"