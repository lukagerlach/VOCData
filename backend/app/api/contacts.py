from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from backend.app.models.contact import Contact
from backend.app.models.dataset import Dataset
from backend.database import get_db

contact_router = APIRouter(prefix="/contacts", tags=["Contacts for Datasets"])


@contact_router.post("/")
async def create_contact(
    contact: Contact, db: Annotated[Session, Depends(get_db)]
):
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@contact_router.get("/")
async def get_all_contacts(db: Session = Depends(get_db)):
    return db.exec(select(Contact)).all()


@contact_router.get("/by-dataset/{dataset_id}")
async def get_contacts_by_dataset_id(
    dataset_id: int, db: Session = Depends(get_db)
):
    statement = select(Dataset).where(Dataset.id == dataset_id)
    dataset = db.exec(statement).one()
    return dataset.contacts
