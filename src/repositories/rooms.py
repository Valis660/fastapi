from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(
            self
    ) -> list[Room]:

            query = select(RoomsOrm)
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(query)

            return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]