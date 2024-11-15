from fastapi import Query, APIRouter, Body
from datetime import date
from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("/hotels",
            summary="Получение данных отелей")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10")

):
    per_page = pagination.per_page or 5

    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=per_page * (pagination.page - 1)
    # )
    return await db.hotels.get_filtered_bytime(
        date_from=date_from,
        date_to=date_to
    )


@router.get("/{hotel_id}",
            summary="Получение данных отеля")
async def get_hotel(db: DBDep, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("",
             summary="Добавить отель")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)

    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}",
            summary="Изменение данных отеля")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных отеля",
           description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def partially_edit_hotels(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPatch
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удалить отель")
async def delete_hotel(db: DBDep, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    return {"status": "OK"}