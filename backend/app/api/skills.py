import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import Skill, User
from app.schemas import SkillCreate, SkillRead, SkillUpdate

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
def create_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = Skill(company_id=current_user.company_id, **payload.model_dump())
    db.add(skill)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Habilidade já existe para esta empresa") from exc
    db.refresh(skill)
    return skill


@router.get("", response_model=list[SkillRead])
def list_skills(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Skill).where(Skill.company_id == current_user.company_id).order_by(Skill.name)
    return list(db.scalars(stmt).all())


@router.patch("/{skill_id}", response_model=SkillRead)
def update_skill(
    skill_id: uuid.UUID,
    payload: SkillUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.scalar(select(Skill).where(Skill.id == skill_id, Skill.company_id == current_user.company_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(skill, key, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Nome de habilidade já cadastrado") from exc
    db.refresh(skill)
    return skill


@router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    skill = db.scalar(select(Skill).where(Skill.id == skill_id, Skill.company_id == current_user.company_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")
    db.delete(skill)
    db.commit()
