from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class MemberModel(Base):

    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    join_date = Column(DateTime)
    expiration_date = Column(DateTime)