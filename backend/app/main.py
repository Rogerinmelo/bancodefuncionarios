from fastapi import FastAPI

from app.api import auth, demands, employee_history, employee_skills, employees, services, skills
from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health", tags=["health"])
def healthcheck():
    return {"status": "ok"}


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(employees.router, prefix=settings.api_prefix)
app.include_router(skills.router, prefix=settings.api_prefix)
app.include_router(employee_skills.router, prefix=settings.api_prefix)

app.include_router(services.router, prefix=settings.api_prefix)

app.include_router(demands.router, prefix=settings.api_prefix)
app.include_router(employee_history.router, prefix=settings.api_prefix)
