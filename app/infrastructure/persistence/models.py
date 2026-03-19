from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class MemberModel(Base):

    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    join_date = Column(DateTime, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False, default="ACTIVE")
    last_benefit = Column(String, nullable=False, default="NONE")
    renewal_count = Column(Integer, nullable=False, default=0)