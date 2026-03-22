from io import BytesIO


def _create_company_and_user(client, company_name: str, email: str, role: str = "admin"):
    company = client.post("/api/v1/auth/register-company", json={"name": company_name})
    company_id = company.json()["id"]
    return _register_user_and_login(client, company_id, email, role)


def _register_user_and_login(client, company_id: str, email: str, role: str):
    client.post(
        "/api/v1/auth/register-user",
        json={
            "company_id": company_id,
            "name": f"{role} user",
            "email": email,
            "password": "senha123",
            "role": role,
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        json={"company_id": company_id, "email": email, "password": "senha123"},
    )
    token = login.json()["access_token"]
    return company_id, {"Authorization": f"Bearer {token}"}


def test_history_cross_tenant_access_is_blocked(client):
    _, headers_a = _create_company_and_user(client, "Empresa A", "admin-a@empresa.com", role="admin")
    _, headers_b = _create_company_and_user(client, "Empresa B", "admin-b@empresa.com", role="admin")

    employee = client.post("/api/v1/employees", headers=headers_a, json={"full_name": "Carlos"}).json()

    list_b = client.get(f"/api/v1/employees/{employee['id']}/history", headers=headers_b)
    assert list_b.status_code == 404


def test_history_upload_rejects_invalid_file_type(client):
    _, headers = _create_company_and_user(client, "Empresa A", "admin@empresa.com", role="admin")
    employee = client.post("/api/v1/employees", headers=headers, json={"full_name": "Ana"}).json()
    history = client.post(
        f"/api/v1/employees/{employee['id']}/history",
        headers=headers,
        json={"comment": "Teste"},
    ).json()

    response = client.post(
        f"/api/v1/employees/{employee['id']}/history/{history['id']}/photos",
        headers=headers,
        files={"file": ("arquivo.txt", BytesIO(b"abc"), "text/plain")},
    )
    assert response.status_code == 400


def test_viewer_cannot_upload_history_photo(client, monkeypatch):
    company_id, admin_headers = _create_company_and_user(client, "Empresa A", "admin@empresa-a.com", role="admin")
    _, viewer_headers = _register_user_and_login(client, company_id, "viewer@empresa-a.com", role="viewer")

    employee = client.post("/api/v1/employees", headers=admin_headers, json={"full_name": "Joana"}).json()
    history = client.post(
        f"/api/v1/employees/{employee['id']}/history",
        headers=admin_headers,
        json={"comment": "Registro"},
    ).json()

    from app.api import employee_history as history_module

    monkeypatch.setattr(
        history_module.storage_service,
        "upload_bytes",
        lambda **kwargs: "http://minio.local/bnc-fotos/photo.jpg",
    )

    photo = client.post(
        f"/api/v1/employees/{employee['id']}/history/{history['id']}/photos",
        headers=viewer_headers,
        files={"file": ("foto.jpg", BytesIO(b"fake-image"), "image/jpeg")},
    )
    assert photo.status_code == 403
