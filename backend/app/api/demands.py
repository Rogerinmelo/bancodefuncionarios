import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db, require_roles
from app.models import (
    Demand,
    DemandSkillRequirement,
    DemandSuggestionSnapshot,
    DemandSuggestionSnapshotItem,
    Employee,
    EmployeeSkill,
    Skill,
    TaskForce,
    TaskForceMember,
    User,
)
from app.schemas import (
    DemandCreate,
    DemandRead,
    DemandSkillRequirementCreate,
    DemandSkillRequirementRead,
    DemandUpdate,
    SuggestionSnapshotRead,
    TaskForceBuildResponse,
    TaskForceMemberRead,
    TeamSuggestionItem,
    TeamSuggestionResponse,
)

router = APIRouter(prefix="/demands", tags=["demands"])


def _load_required_skill_weights(db: Session, demand_id: uuid.UUID) -> dict[uuid.UUID, int]:
    requirements = list(
        db.scalars(
            select(DemandSkillRequirement).where(
                DemandSkillRequirement.demand_id == demand_id,
                DemandSkillRequirement.required.is_(True),
            )
        ).all()
    )
    return {req.skill_id: req.weight for req in requirements}


@router.post("", response_model=DemandRead, status_code=status.HTTP_201_CREATED)
def create_demand(
    payload: DemandCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "gestor")),
):
    demand = Demand(company_id=current_user.company_id, **payload.model_dump())
    db.add(demand)
    db.commit()
    db.refresh(demand)
    return demand


@router.get("", response_model=list[DemandRead])
def list_demands(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Demand).where(Demand.company_id == current_user.company_id).order_by(Demand.created_at.desc())
    return list(db.scalars(stmt).all())


@router.get("/{demand_id}", response_model=DemandRead)
def get_demand(demand_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    demand = db.scalar(select(Demand).where(Demand.id == demand_id, Demand.company_id == current_user.company_id))
    if not demand:
        raise HTTPException(status_code=404, detail="Demanda não encontrada")
    return demand


@router.patch("/{demand_id}", response_model=DemandRead)
def update_demand(
    demand_id: uuid.UUID,
    payload: DemandUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "gestor")),
):
    demand = db.scalar(select(Demand).where(Demand.id == demand_id, Demand.company_id == current_user.company_id))
    if not demand:
        raise HTTPException(status_code=404, detail="Demanda não encontrada")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(demand, key, value)
    db.commit()
    db.refresh(demand)
    return demand


@router.post("/{demand_id}/skills", response_model=DemandSkillRequirementRead, status_code=status.HTTP_201_CREATED)
def add_demand_skill_requirement(
    demand_id: uuid.UUID,
    payload: DemandSkillRequirementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "gestor")),
):
    demand = db.scalar(select(Demand).where(Demand.id == demand_id, Demand.company_id == current_user.company_id))
    if not demand:
        raise HTTPException(status_code=404, detail="Demanda não encontrada")

    skill = db.scalar(select(Skill).where(Skill.id == payload.skill_id, Skill.company_id == current_user.company_id))
    if not skill:
        raise HTTPException(status_code=404, detail="Habilidade não encontrada")

    existing = db.scalar(
        select(DemandSkillRequirement).where(
            DemandSkillRequirement.demand_id == demand_id,
            DemandSkillRequirement.skill_id == payload.skill_id,
        )
    )
    if existing:
        raise HTTPException(status_code=409, detail="Requisito já cadastrado")

    requirement = DemandSkillRequirement(demand_id=demand_id, **payload.model_dump())
    db.add(requirement)
    db.commit()
    db.refresh(requirement)
    return requirement


@router.delete("/{demand_id}/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_demand_skill_requirement(
    demand_id: uuid.UUID,
    skill_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "gestor")),
):
    demand = db.scalar(select(Demand).where(Demand.id == demand_id, Demand.company_id == current_user.company_id))
    if not demand:
        raise HTTPException(status_code=404, detail="Demanda não encontrada")

    requirement = db.scalar(
        select(DemandSkillRequirement).where(
            DemandSkillRequirement.demand_id == demand_id,
            DemandSkillRequirement.skill_id == skill_id,
        )
    )
    if not requirement:
        raise HTTPException(status_code=404, detail="Requisito não encontrado")
    db.delete(requirement)
    db.commit()


@router.post("/{demand_id}/suggest-team", response_model=TeamSuggestionResponse)
def suggest_team(
    demand_id: uuid.UUID,
    top_n: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    demand = db.scalar(select(Demand).where(Demand.id == demand_id, Demand.company_id == current_user.company_id))
    if not demand:
        raise HTTPException(status_code=404, detail="Demanda não encontrada")

    required_skill_ids = _load_required_skill_weights(db, demand_id)
    employees = list(
        db.scalars(
            select(Employee).where(Employee.company_id == current_user.company_id, Employee.is_active.is_(True))
        ).all()
    )

    ranking: list[TeamSuggestionItem] = []
    total_required = len(required_skill_ids)

    for employee in employees:
        emp_skills = list(db.scalars(select(EmployeeSkill).where(EmployeeSkill.employee_id == employee.id)).all())
        emp_map = {es.skill_id: es for es in emp_skills}
        matched = 0
        score = 0.0

        for skill_id, weight in required_skill_ids.items():
            es = emp_map.get(skill_id)
            if es:
                matched += 1
                years = float(es.years_experience) if es.years_experience is not None else 0.0
                score += float(weight) * (1.0 + (years / 10.0))

        ranking.append(
            TeamSuggestionItem(
                employee_id=employee.id,
                employee_name=employee.full_name,
                score=round(score, 2),
                matched_required_skills=matched,
                total_required_skills=total_required,
            )
        )

    ranking.sort(key=lambda item: (item.matched_required_skills, item.score), reverse=True)
    ranking = ranking[:top_n]

    latest_version = db.scalar(
        select(func.max(DemandSuggestionSnapshot.version)).where(DemandSuggestionSnapshot.demand_id == demand_id)
    )
    new_version = (latest_version or 0) + 1
    snapshot = DemandSuggestionSnapshot(demand_id=demand_id, version=new_version)
    db.add(snapshot)
    db.flush()

    for item in ranking:
        db.add(
            DemandSuggestionSnapshotItem(
                snapshot_id=snapshot.id,
                employee_id=item.employee_id,
                employee_name=item.employee_name,
                score=item.score,
                matched_required_skills=item.matched_required_skills,
                total_required_skills=item.total_required_skills,
            )
        )
    db.commit()

    return TeamSuggestionResponse(demand_id=demand.id, ranking=ranking)


@router.get("/{demand_id}/suggestions/latest", response_model=SuggestionSnapshotRead)
def get_latest_suggestion_snapshot(
    demand_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    demand = db.scalar(select(Demand).where(Demand.id == demand_id, Demand.company_id == current_user.company_id))
    if not demand:
        raise HTTPException(status_code=404, detail="Demanda não encontrada")

    snapshot = db.scalar(
        select(DemandSuggestionSnapshot)
        .where(DemandSuggestionSnapshot.demand_id == demand_id)
        .order_by(DemandSuggestionSnapshot.version.desc())
    )
    if not snapshot:
        raise HTTPException(status_code=404, detail="Nenhum snapshot encontrado")

    items = list(
        db.scalars(
            select(DemandSuggestionSnapshotItem)
            .where(DemandSuggestionSnapshotItem.snapshot_id == snapshot.id)
            .order_by(DemandSuggestionSnapshotItem.score.desc())
        ).all()
    )

    ranking = [
        TeamSuggestionItem(
            employee_id=item.employee_id,
            employee_name=item.employee_name,
            score=float(item.score),
            matched_required_skills=item.matched_required_skills,
            total_required_skills=item.total_required_skills,
        )
        for item in items
    ]
    return SuggestionSnapshotRead(
        id=snapshot.id,
        demand_id=snapshot.demand_id,
        version=snapshot.version,
        created_at=snapshot.created_at,
        ranking=ranking,
    )


@router.post("/{demand_id}/build-task-force", response_model=TaskForceBuildResponse)
def build_task_force(
    demand_id: uuid.UUID,
    team_size: int = 3,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "gestor")),
):
    demand = db.scalar(select(Demand).where(Demand.id == demand_id, Demand.company_id == current_user.company_id))
    if not demand:
        raise HTTPException(status_code=404, detail="Demanda não encontrada")

    required_skill_weights = _load_required_skill_weights(db, demand_id)
    uncovered = set(required_skill_weights.keys())

    employees = list(
        db.scalars(
            select(Employee).where(Employee.company_id == current_user.company_id, Employee.is_active.is_(True))
        ).all()
    )

    employee_skills_map: dict[uuid.UUID, dict[uuid.UUID, EmployeeSkill]] = {}
    for employee in employees:
        skills = list(db.scalars(select(EmployeeSkill).where(EmployeeSkill.employee_id == employee.id)).all())
        employee_skills_map[employee.id] = {s.skill_id: s for s in skills}

    selected: list[Employee] = []
    while uncovered and len(selected) < team_size:
        best_employee = None
        best_gain = -1.0

        for employee in employees:
            if employee in selected:
                continue
            emp_skills = employee_skills_map.get(employee.id, {})
            gain = 0.0
            for skill_id in uncovered:
                es = emp_skills.get(skill_id)
                if es:
                    years = float(es.years_experience) if es.years_experience is not None else 0.0
                    gain += float(required_skill_weights[skill_id]) * (1.0 + years / 10.0)
            if gain > best_gain:
                best_gain = gain
                best_employee = employee

        if not best_employee or best_gain <= 0:
            break

        selected.append(best_employee)
        best_skills = employee_skills_map[best_employee.id]
        uncovered = {skill_id for skill_id in uncovered if skill_id not in best_skills}

    task_force = TaskForce(demand_id=demand_id, name=f"Força-tarefa demanda {demand_id}")
    db.add(task_force)
    db.flush()

    members: list[TaskForceMemberRead] = []
    for employee in selected:
        db.add(TaskForceMember(task_force_id=task_force.id, employee_id=employee.id, role_in_team="membro"))
        matched_skills = [
            skill_id
            for skill_id in required_skill_weights.keys()
            if skill_id in employee_skills_map.get(employee.id, {})
        ]
        members.append(
            TaskForceMemberRead(
                employee_id=employee.id,
                employee_name=employee.full_name,
                matched_skills=matched_skills,
            )
        )

    db.commit()

    total_required = len(required_skill_weights)
    covered = total_required - len(uncovered)
    return TaskForceBuildResponse(
        demand_id=demand_id,
        task_force_id=task_force.id,
        task_force_name=task_force.name,
        covered_required_skills=covered,
        total_required_skills=total_required,
        members=members,
    )
