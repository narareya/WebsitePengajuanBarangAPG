from app.config.database import SessionLocal
from app.models import Departement, User, RequestModel, RequestDetail
from app.utils.security import hash_password

db = SessionLocal()

db.query(User).delete()
db.query(Departement).delete()
db.commit()

Departements_data = [
    {"departement_code": "IT", "departement_name": "IT", "departement_status": "active"},
    {"departement_code": "FIN", "departement_name": "Finance", "departement_status": "active"},
    {"departement_code": "HR", "departement_name": "Human Resource", "departement_status": "active"},
]
Departements = [Departement(**d) for d in Departements_data]
db.add_all(Departements)
db.commit()

users_data = [
    {"name": "Admin APG", "email": "admin@apg.com", "password": hash_password("admin123"), "role": "admin", "departement_id": Departements[0].departement_id, "user_status": "active"},
    {"name": "Budi Manager", "email": "budi@apg.com", "password": hash_password("budi123"), "role": "manager", "departement_id": Departements[1].departement_id, "user_status": "active"},
    {"name": "Siti Employee", "email": "siti@apg.com", "password": hash_password("siti123"), "role": "employee", "departement_id": Departements[2].departement_id, "user_status": "active"},
]
users = [User(**u) for u in users_data]
db.add_all(users)
db.commit()

db.close()
print("Seeding success.")