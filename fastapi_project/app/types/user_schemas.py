from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """Schema base para dados do usuário."""
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    """Schema para criação de um novo usuário."""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """Schema para atualização de um usuário existente."""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    """Schema para a resposta da API ao retornar um usuário."""
    id: int

    class Config:
        from_attributes = True