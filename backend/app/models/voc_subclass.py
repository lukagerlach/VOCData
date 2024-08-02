from sqlmodel import Field, SQLModel

from backend.app.models.associations import DatasetVocSubclassLink


class VocSubclass(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="voc_subclasses", link_model=DatasetVocSubclassLink
    )
