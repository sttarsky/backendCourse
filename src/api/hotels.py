from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import check_dates, ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelADD, HotelPATCH
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Адрес отеля"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-11-01"),
        date_to: date = Query(example="2024-11-30"),
):
    return await HotelService(db).get_filtered_by_time(pagination,
                                                       location,
                                                       title,
                                                       date_from,
                                                       date_to)


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_one_or_none(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_one(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelADD = Body(
            openapi_examples={
                "1": {
                    "summary": "Сочи",
                    "value": {
                        "title": "Отель Rich 5 звезд у моря",
                        "location": "Сочи,ул. Моря, 1",
                    },
                },
                "2": {
                    "summary": "Дубай",
                    "value": {
                        "title": "Отель Relax resort у фонтана",
                        "location": "Дубай, ул. Шейха, 2",
                    },
                },
            }
        ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Полное обновление отеля")
async def put_hotel(hotel_id: int, hotel_data: HotelADD, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "ok"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление отеля",
    description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>",
)
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "ok"}


@router.delete("/{hotel_id}")
async def del_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "ok"}
