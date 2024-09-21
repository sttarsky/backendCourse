from fastapi import APIRouter, Query, Body
from pydantic import BaseModel

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

class Hotel(BaseModel):
    title: str
    name: str

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
def patch_hotel(hotel_id: int, title: str | None = Body(), name: str | None = Body()):
    if title and name:
        return put_hotel(hotel_id, title, name)
    else:
        global hotels
        for hotel in hotels:
            if hotel.get("id") == hotel_id:
                if title:
                    hotel["title"] = title
                if name:
                    hotel["name"] = name
                return {"status": "ok"}
            else:
                return {"status": "error"}


@router.delete("/{hotel_id}")
def del_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel.get("id") != hotel_id]
    return {"status": "ok"}