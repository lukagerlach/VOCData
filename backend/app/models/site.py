from geoalchemy2 import Geometry
from geojson_pydantic import Point
from sqlalchemy import event
from sqlmodel import Column, Field, Relationship, SQLModel

from backend.app.utils.geometry_utils import (  # noqa: E501
    geojson_to_geometry,
    geometry_to_geojson,
)


class Site(SQLModel, table=True):
    """
    Represents a site.

    This class models a site where datasets are collected.

    :param id: The unique identifier of the site.
    :type id: int
    :param name: The name of the site.
    :type name: str
    :param region: The region where the site is located.
    :type region: str
    :param country: The country where the site is located.
    :type country: str
    :param typology: The typology of the site.
    :type typology: str
    :param geo_location: The geographical location of the site.
    :type geo_location: Point
    :param datasets: The datasets associated with the site.
    :type datasets: list[Dataset]
    """

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
