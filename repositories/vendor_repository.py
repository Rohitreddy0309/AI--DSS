from sqlalchemy.orm import Session
from models.vendors import Vendors


def get_all_vendors(db: Session):
     return db.query(Vendors).all()

def add_new_vendor(db:Session,vendor:Vendors):
     db.add(vendor)
     db.commit()
     db.refresh(vendor)
     return vendor
 
    