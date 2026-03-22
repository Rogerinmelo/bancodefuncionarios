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
    return company_id, {"Authorization": f"Bearer {access}"}


def test_employee_isolation_between_companies(client):
    _, headers_a = _register_and_login(client, "Empresa A", "a@empresa.com")
    _, headers_b = _register_and_login(client, "Empresa B", "b@empresa.com")

    created = client.post(
        "/api/v1/employees",
        json={"full_name": "Funcionario A", "cpf": "12345678901"},
        headers=headers_a,
    )
    assert created.status_code == 201
    employee_id = created.json()["id"]

    list_b = client.get("/api/v1/employees", headers=headers_b)
    assert list_b.status_code == 200
    assert list_b.json() == []

    detail_b = client.get(f"/api/v1/employees/{employee_id}", headers=headers_b)
    assert detail_b.status_code == 404
