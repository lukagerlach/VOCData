from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.models.voc import Voc
from backend.app.models.voc_subclass import VocSubclass
from backend.app.utils.query_utils import (
    get_all_voc_subclass_ancestor_ids_by_voc_subclass_id,
)
from backend.database import get_db

voc_router = APIRouter(
    prefix="/vocs", tags=["Volatile Organic Compounds (VOCs)"]
)


@voc_router.post("/")
async def create_voc(voc: Voc, db: Annotated[Session, Depends(get_db)]):
    db.add(voc)
    db.commit()
    db.refresh(voc)
    return voc


@voc_router.get("/")
async def get_vocs(db: Annotated[Session, Depends(get_db)]):
    return db.query(Voc).all()


@voc_router.get("/by-subclass/{subclass-name}")
async def get_vocs_by_subclass_name(
    subclass_name: str, db: Annotated[Session, Depends(get_db)]
):
    # get subclass id from name
    subclass_id = (
        db.exec(select(VocSubclass).where(VocSubclass.name == subclass_name))
        .one()
        .id
    )
    vocs = db.exec(select(Voc)).all()
    relevant_vocs = []
    for voc in vocs:
        ancestor_ids = get_all_voc_subclass_ancestor_ids_by_voc_subclass_id(
            voc.voc_subclass.id, db
        )
        if subclass_id in ancestor_ids:
            relevant_vocs.append(voc)

    if not relevant_vocs:
        raise HTTPException(
            status_code=404,
            detail="No vocs available for the specified VOC subclass",
        )

    return relevant_vocs
