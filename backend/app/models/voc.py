from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetVocLink
from backend.app.models.voc_subclass import VocSubclass


class Voc(SQLModel, table=True):
    """
    Represents a VOC (Volatile Organic Compound).

    This class models a VOC and its relationship with datasets \
    and VOC subclasses.

    :param id: The unique identifier of the VOC.
    :type id: int
    :param voc_subclass_id: The ID of the associated VOC subclass.
    :type voc_subclass_id: int
    :param name: The name of the VOC
    :type name: str
    :param datasets: The datasets associated with this VOC.
    :type datasets: list[Dataset]
    """

    id: int | None = Field(default=None, primary_key=True)
    voc_subclass_id: int | None = Field(
        default=None, foreign_key="vocsubclass.id"
    )
    voc_subclass: VocSubclass | None = Relationship(back_populates="vocs")
    name: str | None = None

    # Link to datasets
    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="vocs", link_model=DatasetVocLink
    )
