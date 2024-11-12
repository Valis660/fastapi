from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Booking


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking

    async def get_all(self) -> list[Booking]:

            query = select(BookingsOrm)
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(query)

            return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]