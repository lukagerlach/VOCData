from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.app.models.publication import Publication
from backend.database import get_db

publication_router = APIRouter(
    prefix="/publications", tags=["Publications Referencing Datasets"]
)


@publication_router.get("/")
async def get_publications(db: Session = Depends(get_db)):
    """
    Retrieve all publications.

    This endpoint retrieves all publications stored in the database.

    :param db: The database session.
    :type db: Session
    :return: A list of all publications.
    :rtype: list[Publication]
    """

    return db.query(Publication).all()


@publication_router.post("/")
async def create_publication(pub: Publication, db: Session = Depends(get_db)):
    """
    Create a new publication.

    This endpoint allows the creation of a new publication in the database.

    :param pub: The publication information to be added.
    :type pub: Publication
    :param db: The database session.
    :type db: Session
    :return: The created publication.
    :rtype: Publication
    """

    db.add(pub)
    db.commit()
    db.refresh(pub)
    return pub
