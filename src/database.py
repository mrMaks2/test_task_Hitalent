from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:ZCegthVty295@postgres/restaurant"  # Здесь необходимо заменить на свои данные

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
