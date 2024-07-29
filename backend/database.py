import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

from backend.app.models.associations import DatasetContactLink  # noqa
from backend.app.models.associations import DatasetPublicationLink  # noqa
from backend.app.models.associations import DatasetVocLink  # noqa
from backend.app.models.contact import Contact  # noqa: F401
from backend.app.models.dataset import Dataset  # noqa: F401
from backend.app.models.publication import Publication  # noqa: F401
from backend.app.models.site import Site  # noqa: F401
from backend.app.models.voc import Voc  # noqa: F401
from backend.app.models.voc_subclass import VocSubclass  # noqa: F401

# load env variables from env file
load_dotenv(dotenv_path="../database.env")

# retrieve the environment variables for the database connection
ENV_POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
ENV_POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
ENV_POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
ENV_POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "db")
ENV_POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# create the database URL
DATABASE_URL = (
    f"postgresql://{ENV_POSTGRES_USER}:{ENV_POSTGRES_PASSWORD}"
    f"@{ENV_POSTGRES_SERVER}:{ENV_POSTGRES_PORT}/{ENV_POSTGRES_DB}"
)


# create the database
def init_db() -> None:
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)
