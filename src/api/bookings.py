from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])



@router.post("",
             summary="Забронировать номер")
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingAddRequest):

    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


