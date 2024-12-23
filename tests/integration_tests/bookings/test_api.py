from datetime import date, timedelta


async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    result = await authenticated_ac.post("/bookings",
                                         json={
                                             "room_id": room_id,
                                             "date_from": str(date.today() + timedelta(days=30)),
                                             "date_to": str(date.today() + timedelta(days=31)),
                                         })

    assert result.status_code == 200
    res = result.json()
    assert isinstance(res,dict)
    assert res["status"] == "ok"
    assert "booking" in res
