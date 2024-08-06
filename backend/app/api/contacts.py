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
    """
    Create a new contact.

    This endpoint allows the creation of a new contact in the database.

    :param contact: The contact information to be added.
    :type contact: Contact
    :param db: The database session.
    :type db: Session
    :return: The created contact.
    :rtype: Contact
    """

    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


@contact_router.get("/")
async def get_all_contacts(db: Session = Depends(get_db)):
    """
    Retrieve all contacts.

    This endpoint retrieves all contacts stored in the database.

    :param db: The database session.
    :type db: Session
    :return: A list of all contacts.
    :rtype: list[Contact]
    """

    return db.exec(select(Contact)).all()


@contact_router.get("/by-dataset/{dataset_id}")
async def get_contacts_by_dataset_id(
    dataset_id: int, db: Session = Depends(get_db)
):
    """
    Retrieve contacts by dataset ID.

    This endpoint retrieves contacts associated with a specific dataset.

    :param dataset_id: The ID of the dataset.
    :type dataset_id: int
    :param db: The database session.
    :type db: Session
    :return: A list of contacts associated with the specified dataset.
    :rtype: list[Contact]
    """

    statement = select(Dataset).where(Dataset.id == dataset_id)
    dataset = db.exec(statement).one()
    return dataset.contacts
