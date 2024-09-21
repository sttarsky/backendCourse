from fastapi import APIRouter, Query, Body
from schemas.hotels import Hotel, HotelPUTCH


router = APIRouter(prefix="/hotels", tags=['Отели'])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Dubai", "name": "dubai"}
]



@router.get('')
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    _hotels = []
    for hotel in hotels:
        if id and hotel.get("id") != id:
            continue
        if title and hotel.get("title") != title:
            continue
        _hotels.append(hotel)

    return _hotels



@router.post("")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append(
        {"id": hotels[-1]["id"] + 1,
         "title": hotel_data.title,
         "name": hotel_data.name
         }
    )
    return {"status": "ok"}


@router.put("/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    update_hotel: list[dict] = [hotel for hotel in hotels if hotel.get("id") == hotel_id]
    if update_hotel:
        update_hotel[0]["title"] = hotel_data.title
        update_hotel[0]["name"] = hotel_data.name
        return {"status": "ok"}
    else:
        return {"status": "error"}


@router.patch("/{hotel_id}", summary='Частичное обновление отелей', description="<h1>Тут мы частично обновляем данные об отеле: можно отправить name, а можно title</h1>")
def patch_hotel(hotel_id: int, hotel_data: HotelPUTCH):
    if hotel_data.title and hotel_data.name:
        return put_hotel(hotel_id, hotel_data.title, hotel_data.name)
    else:
        global hotels
        for hotel in hotels:
            if hotel.get("id") == hotel_id:
                if hotel_data.title:
                    hotel["title"] = hotel_data.title
                if hotel_data.name:
                    hotel["name"] = hotel_data.name
                return {"status": "ok"}
            else:
                return {"status": "error"}


@router.delete("/{hotel_id}")
def del_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel.get("id") != hotel_id]
    return {"status": "ok"}