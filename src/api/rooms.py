from fastapi import Query, APIRouter, Body


from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomPATCH, RoomAdd

router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotel_id}/",
            summary="Получение данных номеров")
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()


@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получение данных номера")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/{hotel_id}",
             summary="Добавить номер")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Стандарт", "value": {
        "hotel_id": 1,
        "title": "Стандартный номер",
        "description": "Просторный номер для двоих с двухспальной кроватью",
        "price": 4800,
        "quantity": 5
    }},
    "2": {"summary": "Люкс", "value": {
        "hotel_id": 2,
        "title": "Номер класса Люкс",
        "description": "Шикарный номер LUXE с потрясающим видом на город",
        "price": 15300,
        "quantity": 2
    }}
})
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/{rooms_id}",
            summary="Изменение данных номера")
async def edit_room(room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/{room_id}",
           summary="Частичное обновление данных номера",
           description="<h1>Тут мы частично обновляем данные о номере: можно отправить name, а можно title</h1>",
)
async def partially_edit_rooms(
        room_id: int,
        room_data: RoomPATCH
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/{room_id}",
               summary="Удалить номер")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}