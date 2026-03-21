import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.deps import get_current_user, get_db, require_roles
from app.models import (
    Demand,
    Employee,
    EmployeeServiceHistory,
    EmployeeServicePhoto,
    Service,
    User,
)
from app.schemas import EmployeeHistoryCreate, EmployeeHistoryPhotoRead, EmployeeHistoryRead
from app.services.storage import storage_service

router = APIRouter(prefix="/employees/{employee_id}/history", tags=["employee-history"])


def _get_employee_or_404(db: Session, employee_id: uuid.UUID, company_id: uuid.UUID) -> Employee:
    employee = db.scalar(select(Employee).where(Employee.id == employee_id, Employee.company_id == company_id))
    if not employee:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return employee


@router.post("", response_model=EmployeeHistoryRead, status_code=status.HTTP_201_CREATED)
def create_history(
    employee_id: uuid.UUID,
    payload: EmployeeHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "gestor")),
):
    _get_employee_or_404(db, employee_id, current_user.company_id)

    if payload.service_id:
        service = db.scalar(select(Service).where(Service.id == payload.service_id, Service.company_id == current_user.company_id))
        if not service:
            raise HTTPException(status_code=404, detail="Serviço não encontrado")

    if payload.demand_id:
        demand = db.scalar(select(Demand).where(Demand.id == payload.demand_id, Demand.company_id == current_user.company_id))
        if not demand:
            raise HTTPException(status_code=404, detail="Demanda não encontrada")

    data = payload.model_dump()
    if data.get("performed_at") is None:
        data["performed_at"] = datetime.utcnow()

    history = EmployeeServiceHistory(employee_id=employee_id, **data)
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


@router.get("", response_model=list[EmployeeHistoryRead])
def list_history(
    employee_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_employee_or_404(db, employee_id, current_user.company_id)
    stmt = (
        select(EmployeeServiceHistory)
        .where(EmployeeServiceHistory.employee_id == employee_id)
        .order_by(EmployeeServiceHistory.performed_at.desc())
    )
    return list(db.scalars(stmt).all())


@router.post("/{history_id}/photos", response_model=EmployeeHistoryPhotoRead, status_code=status.HTTP_201_CREATED)
def upload_history_photo(
    employee_id: uuid.UUID,
    history_id: uuid.UUID,
    file: UploadFile = File(...),
    caption: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "gestor")),
):
    _get_employee_or_404(db, employee_id, current_user.company_id)

    history = db.scalar(
        select(EmployeeServiceHistory).where(
            EmployeeServiceHistory.id == history_id,
            EmployeeServiceHistory.employee_id == employee_id,
        )
    )
    if not history:
        raise HTTPException(status_code=404, detail="Histórico não encontrado")

    allowed_types = {mime.strip() for mime in settings.allowed_upload_mime_types.split(",") if mime.strip()}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido")

    content = file.file.read()
    if len(content) > settings.max_upload_size_bytes:
        raise HTTPException(status_code=400, detail="Arquivo excede tamanho máximo permitido")

    file_url = storage_service.upload_bytes(
        content=content,
        original_filename=file.filename,
        content_type=file.content_type,
    )

    photo = EmployeeServicePhoto(history_id=history_id, file_url=file_url, caption=caption)
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo
