def _register_and_login(client, company_name: str, email: str):
    company = client.post(
        "/api/v1/auth/register-company",
        json={"name": company_name, "cnpj": None},
    )
    company_id = company.json()["id"]

    client.post(
        "/api/v1/auth/register-user",
        json={
            "company_id": company_id,
            "name": f"Admin {company_name}",
            "email": email,
            "password": "senha123",
            "role": "admin",
        },
    )

    login = client.post(
        "/api/v1/auth/login",
        json={
            "company_id": company_id,
            "email": email,
            "password": "senha123",
        },
    )
    access = login.json()["access_token"]
    return {"Authorization": f"Bearer {access}"}


def test_services_crud_and_uniqueness(client):
    headers = _register_and_login(client, "Empresa A", "admin@a.com")

    created = client.post(
        "/api/v1/services",
        headers=headers,
        json={"name": "Instalação elétrica", "description": "Serviço residencial"},
    )
    assert created.status_code == 201
    service_id = created.json()["id"]

    duplicate = client.post(
        "/api/v1/services",
        headers=headers,
        json={"name": "Instalação elétrica", "description": "Duplicado"},
    )
    assert duplicate.status_code == 409

    listed = client.get("/api/v1/services", headers=headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.patch(
        f"/api/v1/services/{service_id}",
        headers=headers,
        json={"description": "Serviço industrial"},
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "Serviço industrial"

    removed = client.delete(f"/api/v1/services/{service_id}", headers=headers)
    assert removed.status_code == 204


def test_services_tenant_isolation(client):
    headers_a = _register_and_login(client, "Empresa A", "a@empresa.com")
    headers_b = _register_and_login(client, "Empresa B", "b@empresa.com")

    created = client.post(
        "/api/v1/services",
        headers=headers_a,
        json={"name": "Pintura predial", "description": None},
    )
    service_id = created.json()["id"]

    list_b = client.get("/api/v1/services", headers=headers_b)
    assert list_b.status_code == 200
    assert list_b.json() == []

    detail_b = client.get(f"/api/v1/services/{service_id}", headers=headers_b)
    assert detail_b.status_code == 404
