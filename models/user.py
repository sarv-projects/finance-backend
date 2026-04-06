from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Literal

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: Literal["viewer", "analyst", "admin"]
    
class User(UserCreate):
    user_id: int
    status: Literal["active", "inactive"] = "active"
    created_at: datetime = Field(default_factory=datetime.now)
    
class UserUpdate(BaseModel):
    status: Literal["active", "inactive"]
