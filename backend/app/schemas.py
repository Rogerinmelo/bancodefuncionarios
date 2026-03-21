import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CompanyCreate(BaseModel):
    name: str
    cnpj: str | None = None


class CompanyRead(BaseModel):
    id: uuid.UUID
    name: str
    cnpj: str | None = None
    created_at: datetime


class UserCreate(BaseModel):
    company_id: uuid.UUID
    name: str
    email: EmailStr
    password: str = Field(min_length=6)
    role: str = "admin"


class UserRead(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    name: str
    email: EmailStr
    role: str


class LoginInput(BaseModel):
    company_id: uuid.UUID
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshInput(BaseModel):
    refresh_token: str


class EmployeeCreate(BaseModel):
    full_name: str
    cpf: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None


class EmployeeUpdate(BaseModel):
    full_name: str | None = None
    cpf: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    is_active: bool | None = None


class EmployeeRead(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    full_name: str
    cpf: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class SkillCreate(BaseModel):
    name: str
    category: str | None = None


class SkillUpdate(BaseModel):
    name: str | None = None
    category: str | None = None


class SkillRead(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    name: str
    category: str | None = None
    created_at: datetime


class EmployeeSkillCreate(BaseModel):
    skill_id: uuid.UUID
    proficiency_level: str
    years_experience: float | None = None
    evidence_notes: str | None = None


class EmployeeSkillRead(BaseModel):
    employee_id: uuid.UUID
    skill_id: uuid.UUID
    proficiency_level: str
    years_experience: float | None = None
    evidence_notes: str | None = None


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None


class ServiceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class ServiceRead(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    name: str
    description: str | None = None
    created_at: datetime


class DemandCreate(BaseModel):
    service_id: uuid.UUID | None = None
    title: str
    description: str | None = None
    type: str = "demanda"
    status: str = "aberta"
    location: str | None = None
    budget: float | None = None


class DemandUpdate(BaseModel):
    service_id: uuid.UUID | None = None
    title: str | None = None
    description: str | None = None
    type: str | None = None
    status: str | None = None
    location: str | None = None
    budget: float | None = None


class DemandRead(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    service_id: uuid.UUID | None = None
    title: str
    description: str | None = None
    type: str
    status: str
    location: str | None = None
    budget: float | None = None
    created_at: datetime


class DemandSkillRequirementCreate(BaseModel):
    skill_id: uuid.UUID
    weight: int = 1
    required: bool = True


class DemandSkillRequirementRead(BaseModel):
    demand_id: uuid.UUID
    skill_id: uuid.UUID
    weight: int
    required: bool


class EmployeeHistoryCreate(BaseModel):
    service_id: uuid.UUID | None = None
    demand_id: uuid.UUID | None = None
    comment: str | None = None
    performed_at: datetime | None = None


class EmployeeHistoryRead(BaseModel):
    id: uuid.UUID
    employee_id: uuid.UUID
    service_id: uuid.UUID | None = None
    demand_id: uuid.UUID | None = None
    comment: str | None = None
    performed_at: datetime


class EmployeeHistoryPhotoRead(BaseModel):
    id: uuid.UUID
    history_id: uuid.UUID
    file_url: str
    caption: str | None = None
    created_at: datetime


class TeamSuggestionItem(BaseModel):
    employee_id: uuid.UUID
    employee_name: str
    score: float
    matched_required_skills: int
    total_required_skills: int


class TeamSuggestionResponse(BaseModel):
    demand_id: uuid.UUID
    ranking: list[TeamSuggestionItem]


class TaskForceMemberRead(BaseModel):
    employee_id: uuid.UUID
    employee_name: str
    matched_skills: list[uuid.UUID]


class TaskForceBuildResponse(BaseModel):
    demand_id: uuid.UUID
    task_force_id: uuid.UUID
    task_force_name: str
    covered_required_skills: int
    total_required_skills: int
    members: list[TaskForceMemberRead]


class SuggestionSnapshotRead(BaseModel):
    id: uuid.UUID
    demand_id: uuid.UUID
    version: int
    created_at: datetime
    ranking: list[TeamSuggestionItem]
