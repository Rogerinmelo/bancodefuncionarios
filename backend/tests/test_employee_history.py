from io import BytesIO


def _register_and_login(client, company_name: str, email: str):
    company = client.post("/api/v1/auth/register-company", json={"name": company_name})
    company_id = company.json()["id"]

    client.post(
        "/api/v1/auth/register-user",
        json={
            "company_id": company_id,
            "name": "Admin",
            "email": email,
            "password": "senha123",
            "role": "admin",
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        json={"company_id": company_id, "email": email, "password": "senha123"},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_employee_history_with_photo_upload(client, monkeypatch):
    headers = _register_and_login(client, "Empresa A", "admin@empresa-a.com")
    employee = client.post("/api/v1/employees", headers=headers, json={"full_name": "Maria"}).json()

    history = client.post(
        f"/api/v1/employees/{employee['id']}/history",
        headers=headers,
        json={"comment": "Executou serviço com qualidade"},
    )
    assert history.status_code == 201
    history_id = history.json()["id"]

    from app.api import employee_history as history_module

    monkeypatch.setattr(
        history_module.storage_service,
        "upload_bytes",
        lambda **kwargs: "http://minio.local/bnc-fotos/photo.jpg",
    )

    photo = client.post(
        f"/api/v1/employees/{employee['id']}/history/{history_id}/photos",
        headers=headers,
        files={"file": ("foto.jpg", BytesIO(b"fake-image"), "image/jpeg")},
        data={"caption": "Antes e depois"},
    )
    assert photo.status_code == 201
    assert "minio.local" in photo.json()["file_url"]
