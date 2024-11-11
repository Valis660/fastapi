from fastapi import APIRouter
from datetime import date

from src.api.dependencies import DBDep
from src.schemas.bookings import BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])



@router.post("/",
             summary="Забронировать номер")
async def booking_room(db: DBDep, room_id: int, date_from: date, date_to: date):
    _booking_data = BookingAdd(hotel_id=hotel_id, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)

    return {"status": "OK", "data": booking}

