from datetime import date

from fastapi import APIRouter, Body
from fastapi import Query

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])



@router.get("/{hotel_id}/rooms",
            summary="Получение данных номеров")
async def get_rooms(db: DBDep,
        hotel_id: int,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10")
):
    return await db.rooms.get_filtered_bytime(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получение данных номера")
async def get_room(db: DBDep, hotel_id: int, room_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms",
             summary="Добавить номер")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "Стандарт", "value": {
        "title": "Стандартный номер",
        "description": "Просторный номер для двоих с двухспальной кроватью",
        "price": 4800,
        "quantity": 5
    }},
    "2": {"summary": "Люкс", "value": {
        "title": "Номер класса Люкс",
        "description": "Шикарный номер LUXE с потрясающим видом на город",
        "price": 15300,
        "quantity": 2
    }}
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Изменение данных номера")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Частичное обновление данных номера",
           description="<h1>Тут мы частично обновляем данные о номере: можно отправить name, а можно title</h1>",
)
async def partially_edit_rooms(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}",
               summary="Удалить номер")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    return {"status": "OK"}