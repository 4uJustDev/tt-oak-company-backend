from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.company import CompanyCreate, CompanyUpdate, CompanyOut
from app.crud import company as crud_company
from typing import List

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyOut)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    return crud_company.create_company(db, company)


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
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    updated = crud_company.update_company(db, company_id, company)
    if not updated:
        raise HTTPException(status_code=404, detail="Company not found")
    return updated


@router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    deleted = crud_company.delete_company(db, company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"message": "Company deleted"}
