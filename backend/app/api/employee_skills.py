import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import Employee, EmployeeSkill, Skill, User
from app.schemas import EmployeeSkillCreate, EmployeeSkillRead

router = APIRouter(prefix="/employees/{employee_id}/skills", tags=["employee-skills"])


def _get_employee_or_404(db: Session, employee_id: uuid.UUID, company_id: uuid.UUID) -> Employee:
    employee = db.scalar(select(Employee).where(Employee.id == employee_id, Employee.company_id == company_id))
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


def _get_skill_or_404(db: Session, skill_id: uuid.UUID, company_id: uuid.UUID) -> Skill:
    skill = db.scalar(select(Skill).where(Skill.id == skill_id, Skill.company_id == company_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")
    return skill


@router.post("", response_model=EmployeeSkillRead, status_code=status.HTTP_201_CREATED)
def add_employee_skill(
    employee_id: uuid.UUID,
    payload: EmployeeSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_employee_or_404(db, employee_id, current_user.company_id)
    _get_skill_or_404(db, payload.skill_id, current_user.company_id)

    exists = db.scalar(
        select(EmployeeSkill).where(EmployeeSkill.employee_id == employee_id, EmployeeSkill.skill_id == payload.skill_id)
    )
    if exists:
        raise HTTPException(status_code=409, detail="Vínculo já existe")

    link = EmployeeSkill(employee_id=employee_id, **payload.model_dump())
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.patch("/{skill_id}", response_model=EmployeeSkillRead)
def update_employee_skill(
    employee_id: uuid.UUID,
    skill_id: uuid.UUID,
    payload: EmployeeSkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_employee_or_404(db, employee_id, current_user.company_id)
    _get_skill_or_404(db, skill_id, current_user.company_id)

    link = db.scalar(
        select(EmployeeSkill).where(EmployeeSkill.employee_id == employee_id, EmployeeSkill.skill_id == skill_id)
    )
    if not link:
        raise HTTPException(status_code=404, detail="Vínculo não encontrado")

    link.proficiency_level = payload.proficiency_level
    link.years_experience = payload.years_experience
    link.evidence_notes = payload.evidence_notes
    db.commit()
    db.refresh(link)
    return link


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee_skill(
    employee_id: uuid.UUID,
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_employee_or_404(db, employee_id, current_user.company_id)
    _get_skill_or_404(db, skill_id, current_user.company_id)

    link = db.scalar(
        select(EmployeeSkill).where(EmployeeSkill.employee_id == employee_id, EmployeeSkill.skill_id == skill_id)
    )
    if not link:
        raise HTTPException(status_code=404, detail="Vínculo não encontrado")

    db.delete(link)
    db.commit()
