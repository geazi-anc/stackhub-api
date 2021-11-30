from pydantic import BaseModel


class Question(BaseModel):
    title: str
    body: str
    published_by: str
