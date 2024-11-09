from pydantic import BaseModel


class Email(BaseModel):
    id: str | None = None
    title: str
    body: str
