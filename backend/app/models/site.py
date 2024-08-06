from geoalchemy2 import Geometry
from geojson_pydantic import Point
from sqlalchemy import event
from sqlmodel import Column, Field, Relationship, SQLModel

from backend.app.utils.geometry_utils import (  # noqa: E501
    geojson_to_geometry,
    geometry_to_geojson,
)


class Site(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str | None = None
    region: str | None = None
    country: str
    typology: str | None = None
    # Use geojson_pydantic Scheme to adhere to GeoJSON standard
    # Use GeoAlchemy2 Column Type here to store values properly
    geo_location: Point | None = Field(
        sa_column=Column(Geometry(geometry_type="POINT", srid=4326)),
        default=None,
    )

    datasets: list["Dataset"] | None = Relationship(  # noqa: F821
        back_populates="site"
    )


def site_before_insert(mapper, connection, target):
    target.geo_location = geojson_to_geometry(target.geo_location)


def site_after_load(target, context):
    target.geo_location = geometry_to_geojson(target.geo_location)


event.listen(Site, "before_insert", site_before_insert)
event.listen(Site, "load", site_after_load)
