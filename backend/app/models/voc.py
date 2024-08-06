from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetVocLink
from backend.app.models.voc_subclass import VocSubclass


class Voc(SQLModel, table=True):
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
