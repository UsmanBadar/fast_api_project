from datetime import datetime
from pydantic import BaseModel, EmailStr



class UserLogin(BaseModel):
    email: EmailStr
    password: str

    
class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserInDB(UserBase):
    id: int
    hashed_password: str
