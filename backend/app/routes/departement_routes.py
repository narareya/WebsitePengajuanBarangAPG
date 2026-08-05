from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.departement_schema import DepartementCreate, DepartementUpdate, DepartementResponse
from app.services import departement_service

router = APIRouter(prefix="/departements", tags=["departements"])

@router.post("/", response_model=DepartementResponse, status_code=201)
def create_departement(data: DepartementCreate, db: Session = Depends(get_db)):
    return departement_service.create_departement(db, data)


@router.get("/", response_model=list[DepartementResponse])
def get_all_departements(db: Session = Depends(get_db)):
    return departement_service.get_all_departements(db)


@router.get("/{departement_id}", response_model=DepartementResponse)
def get_departement(departement_id: int, db: Session = Depends(get_db)):
    departement = departement_service.get_departement(db, departement_id)
    if departement is None:
        raise HTTPException(status_code=404, detail="Departement tidak ditemukan")
    return departement


@router.patch("/{departement_id}", response_model=DepartementResponse)
def update_departement(departement_id: int, data: DepartementUpdate, db: Session = Depends(get_db)):
    departement = departement_service.update_departement(db, departement_id, data)
    if departement is None:
        raise HTTPException(status_code=404, detail="Departement tidak ditemukan")
    return departement


@router.delete("/{departement_id}", status_code=204)
def delete_departement(departement_id: int, db: Session = Depends(get_db)):
    success = departement_service.delete_departement(db, departement_id)
    if not success:
        raise HTTPException(status_code=404, detail="departement tidak ditemukan")