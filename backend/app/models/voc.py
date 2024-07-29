from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetVocLink


class Voc(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    voc_subclass_id: int = Field(default=None, foreign_key="vocsubclass.id")
    name: str

    # Link to datasets
    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="vocs", link_model=DatasetVocLink
    )
