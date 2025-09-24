from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.user_routes import user_router
from app.utils.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida para eventos de startup e shutdown.
    """
    # Lógica de startup
    async with engine.begin() as conn:
        # Em um ambiente de produção, você usaria Alembic para migrações.
        # await conn.run_sync(Base.metadata.drop_all) # Para testes
        await conn.run_sync(Base.metadata.create_all)
    print("Startup complete. Database tables created.")
    
    yield
    
    # Lógica de shutdown
    await engine.dispose()
    print("Shutdown complete. Database connection closed.")

# Criação da instância principal da aplicação
app = FastAPI(
    title="API Escalável com FastAPI",
    description="Um exemplo seguindo as melhores práticas de desenvolvimento.",
    version="1.0.0",
    lifespan=lifespan
)

# Inclusão dos routers
app.include_router(user_router)

@app.get("/", tags=["Root"])
async def read_root():
    """
    Endpoint raiz para verificar o status da API.
    """
    return {"status": "API está funcionando corretamente!"}