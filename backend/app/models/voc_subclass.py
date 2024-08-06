from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetVocSubclassLink


class VocSubclass(SQLModel, table=True):
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
