from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyOut
from app.crud import company as crud_company
from typing import List
from app.core.auth import get_current_user_dep
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyOut)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    # Проверка на дубликат имени
    existing = crud_company.get_company_by_name(db, company.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with the same name already exists",
        )
    try:
        return crud_company.create_company(db, company)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with the same name already exists",
        )


@router.get("/", response_model=List[CompanyOut])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_company.get_companies(db, skip=skip, limit=limit)


@router.get("/{company_id}", response_model=CompanyOut)
def read_company(company_id: int, db: Session = Depends(get_db)):
    db_company = crud_company.get_company(db, company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company


@router.patch("/{company_id}", response_model=CompanyOut)
def update_company(
    company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)
):
    # Если обновляется имя, проверяем дубликаты
    update_data = company.dict(exclude_unset=True)
    if "name" in update_data:
        existing = crud_company.get_company_by_name(db, update_data["name"])
        if existing and existing.id != company_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company with the same name already exists",
            )
    try:
        updated = crud_company.update_company(db, company_id, company)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company with the same name already exists",
        )
    if not updated:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated


@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_dep),
):
    deleted = crud_company.delete_company(db, company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted"}
