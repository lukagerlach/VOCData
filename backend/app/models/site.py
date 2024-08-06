from geoalchemy2 import Geometry
from geojson_pydantic import Point
from sqlmodel import Column, Field, Relationship, SQLModel


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
