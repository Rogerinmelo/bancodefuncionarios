def test_auth_register_login_me(client):
    company_response = client.post(
        "/api/v1/auth/register-company",
        json={"name": "Empresa A", "cnpj": "12345678000199"},
    )
    assert company_response.status_code == 201
    company_id = company_response.json()["id"]

    register_user_response = client.post(
        "/api/v1/auth/register-user",
        json={
            "company_id": company_id,
            "name": "Admin A",
            "email": "admin@empresa-a.com",
            "password": "senha123",
            "role": "admin",
        },
    )
    assert register_user_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "company_id": company_id,
            "email": "admin@empresa-a.com",
            "password": "senha123",
        },
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    assert "access_token" in tokens
    assert "refresh_token" in tokens

    me_response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "admin@empresa-a.com"
