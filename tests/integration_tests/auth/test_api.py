import pytest


@pytest.mark.parametrize("email, password, nickname, surname", [
    ("test@test.ru", "123456", "Test", "Test2")
])
async def test_full_auth(email, password, nickname, surname, ac):
    result = await ac.post("/auth/registration",
                           json={
                               "email": email,
                               "password": password,
                               "nickname": nickname,
                               "surname": surname,
                           })
    assert result.status_code == 200
    assert result.json().get("status") == "ok"
    await ac.post("/auth/login",
                  json={
                      "email": email,
                      "password": password,
                  })
    assert ac.cookies.get("access_token")
    user_result = await ac.get("/auth/me",
                               cookies=ac.cookies)
    assert user_result.json().get("email") == email
    await ac.post("/auth/logout", cookies=ac.cookies)
    assert ac.cookies.get("access_token") is None
