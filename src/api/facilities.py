import json
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import Facility, FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Услуги"])


@router.get("")
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        print("ИДУ В БАЗУ ДАННЫХ")
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, 10)
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts

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