from sqlmodel import Field, Relationship, SQLModel

from backend.app.models.associations import DatasetContactLink


class Contact(SQLModel, table=True):
    """
    Represents a contact.

    This class models the contact information related to datasets.

    :param id: The unique identifier of the contact.
    :type id: int
    :param name: The name of the contact.
    :type name: str
    :param email: The email of the contact.
    :type email: str
    :param phone: The phone number of the contact.
    :type phone: str
    :param datasets: The datasets associated with this contact.
    :type datasets: list[Dataset]
    """

    id: int = Field(default=None, primary_key=True)
    name: str
    email: str | None = None
    phone: str | None = None

    # link to datasets
    datasets: list["Dataset"] = Relationship(  # noqa: F821
        back_populates="contacts", link_model=DatasetContactLink
    )
