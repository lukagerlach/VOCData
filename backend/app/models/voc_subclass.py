from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetVocSubclassLink


class VocSubclass(SQLModel, table=True):
    """
    VOC Subclass model representing a subclass of VOC.

    :param id: The unique identifier for the VOC subclass.
    :type id: int
    :param parent_voc_category_id: The ID of the parent VOC category.
    :type parent_voc_category_id: int
    :param parent_voc_category: The parent VOC category.
    :type parent_voc_category: Optional["VocSubclass"]
    :param child_voc_categories: List of child VOC categories.
    :type child_voc_categories: list["VocSubclass"]
    :param vocs: List of VOCs associated with the VOC subclass.
    :type vocs: list["Voc"]
    :param name: The name of the VOC subclass.
    :type name: str
    :param datasets: List of datasets associated with the VOC subclass.
    :type datasets: list["Dataset"]
    """

    id: int = Field(default=None, primary_key=True)
    parent_voc_category_id: int | None = Field(
        default=None, foreign_key="vocsubclass.id"
    )
    parent_voc_category: Optional["VocSubclass"] | None = Relationship(
        back_populates="child_voc_categories",
        sa_relationship_kwargs=dict(remote_side="VocSubclass.id"),
    )
    child_voc_categories: list["VocSubclass"] = Relationship(
        back_populates="parent_voc_category"
    )
    vocs: list["Voc"] | None = Relationship(  # noqa: F821
        back_populates="voc_subclass"
    )
    name: str

    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="voc_subclasses", link_model=DatasetVocSubclassLink
    )
