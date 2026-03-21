import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models import Service, User
from app.schemas import ServiceCreate, ServiceRead, ServiceUpdate

router = APIRouter(prefix="/services", tags=["services"])


@router.post("", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(
    payload: ServiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = Service(company_id=current_user.company_id, **payload.model_dump())
    db.add(service)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Serviço já existe para esta empresa") from exc
    db.refresh(service)
    return service


@router.get("", response_model=list[ServiceRead])
def list_services(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Service).where(Service.company_id == current_user.company_id).order_by(Service.name)
    return list(db.scalars(stmt).all())


@router.get("/{service_id}", response_model=ServiceRead)
def get_service(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = db.scalar(select(Service).where(Service.id == service_id, Service.company_id == current_user.company_id))
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return service


@router.patch("/{service_id}", response_model=ServiceRead)
def update_service(
    service_id: uuid.UUID,
    payload: ServiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = db.scalar(select(Service).where(Service.id == service_id, Service.company_id == current_user.company_id))
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, key, value)

    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Nome de serviço já cadastrado") from exc
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = db.scalar(select(Service).where(Service.id == service_id, Service.company_id == current_user.company_id))
    if not service:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    db.delete(service)
    db.commit()
