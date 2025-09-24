from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()

engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

# Dependência para obter a sessão do banco de dados
async def get_db_session() -> AsyncSession:
    """
    Cria e fornece uma sessão de banco de dados assíncrona por requisição.
    """
    async with AsyncSessionLocal() as session:
        yield session