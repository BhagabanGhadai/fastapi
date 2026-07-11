async def test_register(client):
    resp = await client.post("/users", json={"email": "a@b.com", "password": "secret123"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == "a@b.com"
    assert "hashed_password" not in body


async def test_register_duplicate_email(client):
    await client.post("/users", json={"email": "a@b.com", "password": "secret123"})
    resp = await client.post("/users", json={"email": "a@b.com", "password": "other456"})
    assert resp.status_code == 409
