import os

from sqlmodel import SQLModel, create_engine

from backend.app.models import Site

# retrive the environment variables for the database connection
ENV_POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
ENV_POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
ENV_POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
ENV_POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "db")
ENV_POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# create the database URL
DATABASE_URL = f"postgresql://{ENV_POSTGRES_USER}:{ENV_POSTGRES_PASSWORD}@{ENV_POSTGRES_SERVER}:{ENV_POSTGRES_PORT}/{ENV_POSTGRES_DB}"


# create the database
def init_db() -> None:
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)
