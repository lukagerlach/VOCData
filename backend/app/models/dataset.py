from datetime import date

from sqlmodel import CheckConstraint, Field, Relationship, SQLModel

from backend.app.enums.time_resolution_unit_enum import TimeResolutionUnitEnum
from backend.app.models.associations import (
    DatasetContactLink,
    DatasetPublicationLink,
    DatasetVocLink,
    DatasetVocSubclassLink,
)
from backend.app.models.contact import Contact
from backend.app.models.publication import Publication
from backend.app.models.site import Site
from backend.app.models.voc import Voc
from backend.app.models.voc_subclass import VocSubclass


class Dataset(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    site_id: int | None = Field(default=None, foreign_key="site.id")
    site: Site = Relationship(back_populates="datasets")
    sampling_period_begin: date | None = None
    sampling_period_end: date | None = None
    time_resolution_unit: TimeResolutionUnitEnum | None = None
    time_resolution_interval: int | None = None
    data_type: str | None = None
    link_to_dataset: str | None = None

    # link to vocs
    vocs: list[Voc] | None = Relationship(
        back_populates="datasets", link_model=DatasetVocLink
    )
    # link to contacts
    contacts: list[Contact] | None = Relationship(
        back_populates="datasets", link_model=DatasetContactLink
    )
    # link to publications
    publications: list[Publication] | None = Relationship(
        back_populates="datasets", link_model=DatasetPublicationLink
    )

    # link to voc subclasses
    voc_subclasses: list[VocSubclass] | None = Relationship(
        back_populates="datasets", link_model=DatasetVocSubclassLink
    )

    # Create database level constraint for period end after period start
    __table_args__ = (
        CheckConstraint(
            "sampling_period_end > sampling_period_begin",
            name="check_end_date_after_start_date",
        ),
    )
