from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from src.database import SessionLocal
from src.models.reservation import Reservation
from src.schemas.reservation import ReservationCreate, Reservation as ReservationResponse

router = APIRouter()

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

@router.get("/", response_model=list[ReservationResponse])
async def read_reservations(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(Reservation.__table__.select().limit(limit).offset(skip))
    return result.scalars().all()

@router.post("/")
async def create_reservation(reservation: ReservationCreate, db: AsyncSession = Depends(get_db)):
    table_reservations = await db.execute(
        Reservation.__table__.select().where(
            Reservation.table_id == reservation.table_id
        ).where(
            Reservation.reservation_time.between(reservation.reservation_time,
                                                  reservation.reservation_time + timedelta(minutes=reservation.duration_minutes))
        )
    )
    if table_reservations.scalars().first():
        raise HTTPException(status_code=409, detail="Стол уже зарезервирован на этот временной интервал")

    db_reservation = Reservation(customer_name=reservation.customer_name,
                                 table_id=reservation.table_id,
                                 reservation_time=reservation.reservation_time,
                                 duration_minutes=reservation.duration_minutes)
    db.add(db_reservation)
    await db.commit()
    await db.refresh(db_reservation)
    return db_reservation

@router.delete("/{reservation_id}")
async def delete_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    reservation = await db.get(Reservation, reservation_id)
    if reservation is None:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    await db.delete(reservation)
    await db.commit()
    return {"detail": "Бронирование удалено"}

class Pass:
    pass