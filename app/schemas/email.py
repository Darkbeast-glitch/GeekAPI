from pydantic import BaseModel


class EmailBase(BaseModel):
    email: str


class EmailCreate(EmailBase):
    pass


class Email(EmailBase):
    id: int

    class Config:
        orm_mode = True
