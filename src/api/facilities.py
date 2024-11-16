from datetime import date
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Услуги"])



@router.get("",
            summary="Получить услугу")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("",
             summary="Добавить услугу")
async def add_facilities(db: DBDep, facility_data: FacilityAdd = Body(openapi_examples={
    "1": {"summary": "Wi-Fi", "value": {
        "title": "Бесплатный интернет",
    }},
    "2": {"summary": "Шведский стол", "value": {
        "title": "Питание по системе шведский стол",
    }}
})
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}