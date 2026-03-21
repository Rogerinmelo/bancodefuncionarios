import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import Employee, User
from app.schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post("", response_model=EmployeeRead, status_code=status.HTTP_201_CREATED)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = Employee(company_id=current_user.company_id, **payload.model_dump())
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("", response_model=list[EmployeeRead])
def list_employees(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    active_only: bool = Query(default=True),
):
    stmt = select(Employee).where(Employee.company_id == current_user.company_id)
    if active_only:
        stmt = stmt.where(Employee.is_active.is_(True))
    return list(db.scalars(stmt.order_by(Employee.full_name)).all())


@router.get("/{employee_id}", response_model=EmployeeRead)
def get_employee(
    employee_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = db.scalar(
        select(Employee).where(Employee.id == employee_id, Employee.company_id == current_user.company_id)
    )
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.patch("/{employee_id}", response_model=EmployeeRead)
def update_employee(
    employee_id: uuid.UUID,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = db.scalar(
        select(Employee).where(Employee.id == employee_id, Employee.company_id == current_user.company_id)
    )
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/{employee_id}", response_model=EmployeeRead)
def inactivate_employee(
    employee_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    employee = db.scalar(
        select(Employee).where(Employee.id == employee_id, Employee.company_id == current_user.company_id)
    )
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    employee.is_active = False
    db.commit()
    db.refresh(employee)
    return employee
