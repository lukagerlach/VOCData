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
    """
    Represents a dataset.

    This class models a dataset and its various attributes.

    :param id: The unique identifier of the dataset.
    :type id: int
    :param site_id: The ID of the associated site.
    :type site_id: int
    :param site: The site associated with the dataset.
    :type site: Site
    :param sampling_period_begin: The start date of the sampling period.
    :type sampling_period_begin: date
    :param sampling_period_end: The end date of the sampling period.
    :type sampling_period_end: date
    :param time_resolution_unit: The unit of time resolution.
    :type time_resolution_unit: TimeResolutionUnitEnum
    :param time_resolution_interval: The interval of time resolution.
    :type time_resolution_interval: int
    :param data_type: The type of data in the dataset.
    :type data_type: str
    :param link_to_dataset: The link to the dataset.
    :type link_to_dataset: str
    :param vocs: The VOCs associated with the dataset.
    :type vocs: list[Voc]
    :param contacts: The contacts associated with the dataset.
    :type contacts: list[Contact]
    :param publications: The publications associated with the dataset.
    :type publications: list[Publication]
    :param voc_subclasses: The VOC subclasses associated with the dataset.
    :type voc_subclasses: list[VocSubclass]
    """

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
