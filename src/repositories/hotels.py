from sqlalchemy import select, func

from src.repositories.base import BaseRepositoriy
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepositoriy):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):

            query = select(HotelsOrm)
            if location:
                query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.strip().lower()}%"))
            if title:
                query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
            query = (
                query
                .limit(limit)
                .offset(offset)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            result = await self.session.execute(query)

            return result.scalars().all()
