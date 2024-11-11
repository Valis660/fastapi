from pydantic import BaseModel
from datetime import date

class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Booking(BookingAdd):
    id: int

