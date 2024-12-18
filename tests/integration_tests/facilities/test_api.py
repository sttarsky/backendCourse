
async def test_api_facilities(ac):
    response = await ac.post(
        "/facilities",
        json={
            "title": "Wi-Fi"
        }
    )
    print(f"{response.json()=}")
    assert response.status_code == 200
    assert await ac.get("/facilities")

