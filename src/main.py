from fastapi import FastAPI
from src.database import engine, Base
from src.routers import tables, reservations
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Таблицы базы данных успешно созданы.")
    except Exception as e:
        logger.error(f"Ошибка создания таблиц базы данных: {e}")

app.include_router(tables.router, prefix="/tables", tags=["tables"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
