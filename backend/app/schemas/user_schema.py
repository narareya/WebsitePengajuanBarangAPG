from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional


class RoleEnum(str, Enum):
    employee = "employee"
    manager = "manager"
    admin = "admin"

class UserStatusEnum(str, Enum):
    active = "active"
    off = "off"

class UserCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    role: RoleEnum
    departement_id: int
    user_status: UserStatusEnum = UserStatusEnum.active

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    role: Optional[RoleEnum] = None
    departement_id: Optional[int] = None
    user_status: Optional[UserStatusEnum] = None


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    role: RoleEnum
    departement_id: int
    user_status: UserStatusEnum

    class Config:
        from_attributes = True