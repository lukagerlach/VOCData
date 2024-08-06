from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from backend.app.models.site import Site
from backend.database import get_db

site_router = APIRouter(prefix="/sites", tags=["Research Sites"])


@site_router.post("/")
async def create_site(site: Site, db: Annotated[Session, Depends(get_db)]):
    """
    Create a new site.

    This endpoint allows the creation of a new research site in the database.

    :param site: The site information to be added.
    :type site: Site
    :param db: The database session.
    :type db: Session
    :return: The created site.
    :rtype: Site
    """

    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@site_router.get("/")
async def get_sites(db: Annotated[Session, Depends(get_db)]):
    """
    Retrieve all sites.

    This endpoint retrieves all research sites stored in the database.

    :param db: The database session.
    :type db: Session
    :return: A list of all sites.
    :rtype: list[Site]
    """

    sites = db.query(Site).all()
    return sites


@site_router.get("/{site-id}")
async def get_site_by_id(site_id: int, db: Annotated[Session, Depends(get_db)]):
    """
    Retrieve a site by its ID.

    This endpoint retrieves a research site by its ID.

    :param site_id: The ID of the site.
    :type site_id: int
    :param db: The database session.
    :type db: Session
    :return: The site with the specified ID.
    :rtype: Site
    """

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
    """
    Retrieve sites within a specified area.

    This endpoint retrieves research sites that are \
    located within a specified bounding box.

    :param min_lon: Minimum longitude of the bounding box.
    :type min_lon: float
    :param min_lat: Minimum latitude of the bounding box.
    :type min_lat: float
    :param max_lon: Maximum longitude of the bounding box.
    :type max_lon: float
    :param max_lat: Maximum latitude of the bounding box.
    :type max_lat: float
    :param db: The database session.
    :type db: Session
    :return: A list of sites within the specified bounding box.
    :rtype: list[Site]
    :raise HTTPException: no Site found in that area
    """

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
