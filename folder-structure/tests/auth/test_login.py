async def test_login_flow(client):
    await client.post("/users", json={"email": "a@b.com", "password": "secret123"})

    resp = await client.post("/auth/login", json={"email": "a@b.com", "password": "secret123"})
    assert resp.status_code == 200
    token = resp.json()["access_token"]

    resp = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "a@b.com"


async def test_login_wrong_password(client):
    await client.post("/users", json={"email": "a@b.com", "password": "secret123"})
    resp = await client.post("/auth/login", json={"email": "a@b.com", "password": "wrong"})
    assert resp.status_code == 401


async def test_me_requires_token(client):
    resp = await client.get("/users/me")
    assert resp.status_code == 401
