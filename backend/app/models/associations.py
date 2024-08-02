from sqlmodel import Field, SQLModel


# Link Table for Dataset Voc Connection
class DatasetVocLink(SQLModel, table=True):
    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    voc_id: int | None = Field(
        default=None, foreign_key="voc.id", primary_key=True
    )
    instrument: str | None = None


# Link Table for Dataset Publication Connection
class DatasetPublicationLink(SQLModel, table=True):
    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    publication_id: int | None = Field(
        default=None, foreign_key="publication.id", primary_key=True
    )


# Link Table for Dataset Contact Connection
class DatasetContactLink(SQLModel, table=True):
    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    contact_id: int | None = Field(
        default=None, foreign_key="contact.id", primary_key=True
    )


# Link Table for Dataset VocSubclass Connection
class DatasetVocSubclassLink(SQLModel, table=True):
    dataset_id: int | None = Field(
        default=None, foreign_key="dataset.id", primary_key=True
    )
    voc_subclass_id: int | None = Field(
        default=None, foreign_key="voc_subclass.id", primary_key=True
    )
