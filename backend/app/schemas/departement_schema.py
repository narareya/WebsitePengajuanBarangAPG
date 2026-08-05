from pydantic import BaseModel

class DepartementCreate(BaseModel):
    departement_code: str
    departement_name: str
    departement_status: str = "active"

class DepartementUpdate(BaseModel):
    departement_code: str | None = None
    departement_name: str | None = None
    departement_status: str | None = None

class DepartementResponse(BaseModel):
    departement_id: int
    departement_code: str
    departement_name: str
    departement_status: str

    class Config: 
        from_attributes = True