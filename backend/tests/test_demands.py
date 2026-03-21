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


def test_demands_crud_requirements_and_suggest_team(client):
    headers = _register_and_login(client, "Empresa A", "admin@empresa-a.com")

    employee = client.post("/api/v1/employees", headers=headers, json={"full_name": "João"}).json()
    skill = client.post("/api/v1/skills", headers=headers, json={"name": "NR10"}).json()
    client.post(
        f"/api/v1/employees/{employee['id']}/skills",
        headers=headers,
        json={"skill_id": skill["id"], "proficiency_level": "avancado", "years_experience": 5},
    )

    demand = client.post(
        "/api/v1/demands",
        headers=headers,
        json={"title": "Licitação elétrica", "type": "licitacao", "status": "aberta"},
    )
    assert demand.status_code == 201
    demand_id = demand.json()["id"]

    req = client.post(
        f"/api/v1/demands/{demand_id}/skills",
        headers=headers,
        json={"skill_id": skill["id"], "weight": 2, "required": True},
    )
    assert req.status_code == 201

    suggest = client.post(f"/api/v1/demands/{demand_id}/suggest-team", headers=headers)
    assert suggest.status_code == 200
    assert len(suggest.json()["ranking"]) == 1
    assert suggest.json()["ranking"][0]["matched_required_skills"] == 1
