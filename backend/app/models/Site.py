from sqlmodel import Field, SQLModel


class Site(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str | None = None
