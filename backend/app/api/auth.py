import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.deps import get_current_user, get_db
from app.models import Company, User
from app.schemas import (
    CompanyCreate,
    CompanyRead,
    LoginInput,
    RefreshInput,
    TokenPair,
    UserCreate,
    UserRead,
)
from app.security import create_access_token, create_refresh_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register-company", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def register_company(payload: CompanyCreate, db: Session = Depends(get_db)):
    company = Company(name=payload.name, cnpj=payload.cnpj)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.post("/register-user", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    company = db.scalar(select(Company).where(Company.id == payload.company_id))
    if not company:
        raise HTTPException(status_code=404, detail="Empresa não encontrada")

    user = User(
        company_id=payload.company_id,
        name=payload.name,
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email já cadastrado para esta empresa") from exc
    db.refresh(user)
    return user


@router.post("/login", response_model=TokenPair)
def login(payload: LoginInput, db: Session = Depends(get_db)):
    user = db.scalar(
        select(User).where(
            User.company_id == payload.company_id,
            User.email == str(payload.email).lower(),
        )
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access = create_access_token(subject=str(user.id), company_id=str(user.company_id))
    refresh = create_refresh_token(subject=str(user.id), company_id=str(user.company_id))
    return TokenPair(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenPair)
def refresh_token(payload: RefreshInput, db: Session = Depends(get_db)):
    try:
        decoded = jwt.decode(payload.refresh_token, settings.jwt_refresh_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Refresh token inválido") from exc

    if decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Token não é refresh token")

    user_id = decoded.get("sub")
    company_id = decoded.get("company_id")
    if not user_id or not company_id:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    user = db.scalar(select(User).where(User.id == uuid.UUID(user_id)))
    if not user or str(user.company_id) != company_id:
        raise HTTPException(status_code=401, detail="Usuário inválido")

    new_access = create_access_token(subject=str(user.id), company_id=str(user.company_id))
    new_refresh = create_refresh_token(subject=str(user.id), company_id=str(user.company_id))
    return TokenPair(access_token=new_access, refresh_token=new_refresh)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)):
    return current_user
