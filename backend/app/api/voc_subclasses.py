from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from backend.app.models.voc import Voc
from backend.app.models.voc_subclass import VocSubclass
from backend.app.utils.query_utils import (
    get_all_voc_subclass_ancestor_ids_by_voc_subclass_id,
)
from backend.database import get_db

voc_subclass_router = APIRouter(
    prefix="/voc-subclasses",
    tags=["VOC Subclasses"],
)


@voc_subclass_router.post("/")
async def create_voc_subclass(
    voc_subclass: VocSubclass, db: Annotated[Session, Depends(get_db)]
):
    db.add(voc_subclass)
    db.commit()
    db.refresh(voc_subclass)


@voc_subclass_router.get("/")
async def get_voc_subclasses(db: Session = Depends(get_db)):
    return db.query(VocSubclass).all()


@voc_subclass_router.get("/by-voc-id/{voc-id}")
async def get_voc_subclasses_by_voc_id(
    voc_id: int, db: Session = Depends(get_db)
):
    try:
        voc = db.exec(select(Voc).where(Voc.id == voc_id)).one()

    except NoResultFound:
        raise HTTPException(
            status_code=404, detail="No VOC found for the given VOC id"
        )

    associated_subclasses_ids = (
        get_all_voc_subclass_ancestor_ids_by_voc_subclass_id(
            voc.voc_subclass_id, db
        )
    )

    associated_subclasses = []
    for subclass_id in associated_subclasses_ids:
        associated_subclasses.append(
            db.exec(
                select(VocSubclass).where(VocSubclass.id == subclass_id)
            ).one()
        )

    if not associated_subclasses:
        raise HTTPException(
            status_code=404, detail="No VOC subclasses found for the given voc"
        )

    return associated_subclasses
