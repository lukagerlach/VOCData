from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.app.models.publication import Publication
from backend.database import get_db

publication_router = APIRouter(
    prefix="/publications", tags=["Publications Referencing Datasets"]
)


@publication_router.get("/")
async def get_publications(db: Session = Depends(get_db)):
    return db.query(Publication).all()


@publication_router.post("/")
async def create_publication(pub: Publication, db: Session = Depends(get_db)):
    db.add(pub)
    db.commit()
    db.refresh(pub)
    return pub
