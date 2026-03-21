def _create_user_and_login(client, company_name: str, email: str, role: str = "admin"):
    company = client.post("/api/v1/auth/register-company", json={"name": company_name})
    company_id = company.json()["id"]

    user = client.post(
        "/api/v1/auth/register-user",
        json={
            "company_id": company_id,
            "name": f"{role} user",
            "email": email,
            "password": "senha123",
            "role": role,
        },
    )
    assert user.status_code == 201

    login = client.post(
        "/api/v1/auth/login",
        json={"company_id": company_id, "email": email, "password": "senha123"},
    )
    token = login.json()["access_token"]
    return company_id, {"Authorization": f"Bearer {token}"}


def test_demands_cross_tenant_forbidden_visibility(client):
    _, headers_a = _create_user_and_login(client, "Empresa A", "admin-a@empresa.com", role="admin")
    _, headers_b = _create_user_and_login(client, "Empresa B", "admin-b@empresa.com", role="admin")

    demand = client.post(
        "/api/v1/demands",
        headers=headers_a,
        json={"title": "Demanda A", "type": "demanda", "status": "aberta"},
    )
    demand_id = demand.json()["id"]

    detail_b = client.get(f"/api/v1/demands/{demand_id}", headers=headers_b)
    assert detail_b.status_code == 404


def test_viewer_cannot_create_or_change_demands(client):
    _, viewer_headers = _create_user_and_login(client, "Empresa Viewer", "viewer@empresa.com", role="viewer")

    create = client.post(
        "/api/v1/demands",
        headers=viewer_headers,
        json={"title": "Demanda Viewer", "type": "demanda", "status": "aberta"},
    )
    assert create.status_code == 403
