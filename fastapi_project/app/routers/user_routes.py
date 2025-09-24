from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.types import user_schemas
from app.utils.database import get_db_session
# Supondo que você tenha um modelo ORM em um arquivo models.py
# from app.models import User

# Mock de um modelo ORM para o exemplo ser executável
from sqlalchemy import Column, Integer, String, Boolean
from app.utils.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


# Criando o router
user_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@user_router.post("/", response_model=user_schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: user_schemas.UserCreate,
    db: AsyncSession = Depends(get_db_session)
) -> User:
    """
    Cria um novo usuário no banco de dados.
    Utiliza guard clauses para validação e tratamento de erro no início.
    """
    # Guard clause para verificar se o usuário já existe
    existing_user_result = await db.execute(select(User).where(User.email == user_data.email))
    if existing_user_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Um usuário com este e-mail já existe."
        )

    # O "happy path" vem por último
    # Em um app real, você faria o hash da senha aqui
    hashed_password = user_data.password + "_hashed" # Mock
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=user_data.is_active
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@user_router.get("/", response_model=List[user_schemas.UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
) -> List[User]:
    """
    Retorna uma lista de todos os usuários com paginação.
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return users

@user_router.get("/{user_id}", response_model=user_schemas.UserResponse)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db_session)
) -> User:
    """
    Busca um usuário específico pelo seu ID.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    # Guard clause para o caso de não encontrar o usuário
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuário com ID {user_id} não encontrado."
        )

    return user