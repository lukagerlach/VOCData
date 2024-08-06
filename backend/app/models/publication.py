from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetPublicationLink


class Publication(SQLModel, table=True):
    """
    Represents a publication.

    This class models a publication that references datasets.

    :param id: The unique identifier of the publication.
    :type id: int
    :param link: The link to the publication.
    :type link: str
    :param datasets: The datasets associated with the publication.
    :type datasets: list[Dataset]
    """

    id: int | None = Field(default=None, primary_key=True)
    link: str

    # link to datasets
    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="publications", link_model=DatasetPublicationLink
    )
