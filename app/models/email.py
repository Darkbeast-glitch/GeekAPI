from sqlalchemy import Column, Integer, String
from database.session import Base


class Email(Base):
    __tablename__ = "emails"
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
