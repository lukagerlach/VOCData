from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetContactLink


class Contact(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str | None = None
    phone: str | None = None

    # link to datasets
    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="contacts", link_model=DatasetContactLink
    )
