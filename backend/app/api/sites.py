from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from backend.app.models.site import Site
from backend.database import get_db

site_router = APIRouter(prefix="/sites", tags=["Research Sites"])


@site_router.post("/", response_model=Site)
async def create_site(site: Site, db: Annotated[Session, Depends(get_db)]):
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@site_router.get("/")
async def get_sites(db: Annotated[Session, Depends(get_db)]):
    sites = db.query(Site).all()
    return sites


@site_router.get("/{site-id}")
async def get_site_by_id(site_id: int, db: Annotated[Session, Depends(get_db)]):
    statement = select(Site).where(Site.id == site_id)
    return db.exec(statement).one()


@site_router.get("/by-area/{min_lon}/{min_lat}/{max_lon}/{max_lat}/")
async def get_sites_by_area(
    min_lon: float,
    min_lat: float,
    max_lon: float,
    max_lat: float,
    db: Annotated[Session, Depends(get_db)],
):
    bbox = (
        f"POLYGON(({min_lon} {min_lat}, {min_lon} {max_lat}, {max_lon}"
        f" {max_lat}, {max_lon} {min_lat}, {min_lon} {min_lat}))"
    )

    statement = select(Site).where(
        Site.func.ST_Within(Site.geo_location, func.ST_GeomFromText(bbox, 4326))
    )

    results = db.exec(statement).all()

    if not results:
        raise HTTPException(
            status_code=404, detail="No site found in the specified area"
        )

    return results
