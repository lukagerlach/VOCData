from sqlmodel import Field, SQLModel


class VocSubclass(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
