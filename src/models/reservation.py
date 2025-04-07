from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from src.database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    reservation_time = Column(DateTime)
    duration_minutes = Column(Integer)

class Pass:
    pass