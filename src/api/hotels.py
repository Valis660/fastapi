from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("/hotels",
            summary="Получение данных отелей")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.delete("/{hotel_id}",
               summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("",
             summary="Добавить отель")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "Отель Сочи 5 звезд у моря",
        "location": "Сочи, ул. Моря, 1"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Отель Дубай у фонтана",
        "location": "Дубай, ул. Шейха, 2"
    }}
})
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
            summary="Изменение данных отеля")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных отеля",
           description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>")
def partially_edit_hotels(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}