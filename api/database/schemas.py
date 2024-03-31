from pydantic import BaseModel
from typing import List, Dict, Optional

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    name: str
    roles: List
    context: Dict
    is_active: bool
    is_company: bool
    created_at: str
    update_at: str
    deleted_at: Optional[str]


    class Config:
        orm_mode = True