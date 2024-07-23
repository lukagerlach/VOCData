from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetPublicationLink


class Publication(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    link: str

    # link to datasets
    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="publications", link_model=DatasetPublicationLink
    )
