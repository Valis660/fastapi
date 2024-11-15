from sqlalchemy import select, func
from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


    async def get_filtered_bytime(
            self,
            date_from: date,
            date_to: date,
            location,
            title,
            limit,
            offset,
) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotel_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotel_ids_to_get))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.strip().lower()}%"))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)

        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

