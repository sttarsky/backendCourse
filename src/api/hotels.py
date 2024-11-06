from datetime import date

from fastapi import APIRouter, Query, Body
from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelADD, HotelPATCH

router = APIRouter(prefix="/hotels", tags=['Отели'])


@router.get('')
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description='Адрес отеля'),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-11-01"),
        date_to: date = Query(example="2024-11-30")
):
    per_page = pagination.per_page or 5
    offset = per_page * (pagination.page - 1)
    return await db.hotels.get_filtered_by_time(date_to=date_to, date_from=date_from)
    # return await db.hotels.get_all(
    #     location=location,
    #     title=title,
    #     limit=per_page,
    #     offset=offset
    # )


@router.get("/{hotel_id}")
async def get_one_or_none(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelADD = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Rich 5 звезд у моря",
            "location": "Сочи,ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Relax resort у фонтана",
            "location": "Дубай, ул. Шейха, 2",
        }
    }
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary='Полное обновление отеля')
async def put_hotel(hotel_id: int, hotel_data: HotelADD, db: DBDep):
    hotel = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "ok", "hotel_data": hotel}


@router.patch("/{hotel_id}", summary='Частичное обновление отеля',
              description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def del_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "ok"}
