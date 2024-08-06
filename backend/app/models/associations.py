from sqlmodel import Field, SQLModel


# Link Table for Dataset Voc Connection
class DatasetVocLink(SQLModel, table=True):
    """
    Link table for Dataset and VOC connection.

    This table establishes a many-to-many relationship \
    between datasets and VOCs.

    :param dataset_id: The ID of the dataset.
    :type dataset_id: int
    :param voc_id: The ID of the VOC.
    :type voc_id: int
    :param instrument: The instrument used for VOC measurement.
    :type instrument: str
    """

    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    voc_id: int | None = Field(
        default=None, foreign_key="voc.id", primary_key=True
    )
    instrument: str | None = None


# Link Table for Dataset Publication Connection
class DatasetPublicationLink(SQLModel, table=True):
    """
    Link table for Dataset and Publication connection.

    This table establishes a many-to-many relationship \
    between datasets and publications.

    :param dataset_id: The ID of the dataset.
    :type dataset_id: int
    :param publication_id: The ID of the publication.
    :type publication_id: int
    """

    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    publication_id: int | None = Field(
        default=None, foreign_key="publication.id", primary_key=True
    )


# Link Table for Dataset Contact Connection
class DatasetContactLink(SQLModel, table=True):
    """
    Link table for Dataset and Contact connection.

    This table establishes a many-to-many relationship \
    between datasets and contacts.

    :param dataset_id: The ID of the dataset.
    :type dataset_id: int
    :param contact_id: The ID of the contact.
    :type contact_id: int
    """

    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    contact_id: int | None = Field(
        default=None, foreign_key="contact.id", primary_key=True
    )


# Link Table for Dataset VocSubclass Connection
class DatasetVocSubclassLink(SQLModel, table=True):
    """
    Link table for Dataset and VOC Subclass connection.

    This table establishes a many-to-many relationship\
     between datasets and VOC subclasses.

    :param dataset_id: The ID of the dataset.
    :type dataset_id: int
    :param voc_subclass_id: The ID of the VOC subclass.
    :type voc_subclass_id: int
    """

    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    voc_subclass_id: int | None = Field(
        default=None, foreign_key="vocsubclass.id", primary_key=True
    )
