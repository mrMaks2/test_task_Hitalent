from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.table import Table
from src.schemas.table import TableCreate, Table as TableResponse

router = APIRouter()

@router.get("/", response_model=list[TableResponse])
async def read_tables(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(Table.__table__.select().limit(limit).offset(skip))
    return result.scalars().all()

@router.post("/", response_model=TableResponse)
async def create_table(table: TableCreate, db: AsyncSession = Depends(get_db)):
    db_table = Table(name=table.name, seats=table.seats, location=table.location)
    db.add(db_table)
    await db.commit()
    await db.refresh(db_table)
    return db_table

@router.delete("/{table_id}")
async def delete_table(table_id: int, db: AsyncSession = Depends(get_db)):
    table = await db.get(Table, table_id)
    if table is None:
        raise HTTPException(status_code=404, detail="Стол не найден")
    await db.delete(table)
    await db.commit()
    return {"detail": "Стол удален"}
