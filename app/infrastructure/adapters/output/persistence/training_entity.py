from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Text

Base = declarative_base()

class TrainingPlanModel(Base):
    __tablename__ = "training_plans"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    member_id   = Column(Integer, nullable=False, index=True)
    member_name = Column(String,  nullable=False)
    weight_kg   = Column(Float,   nullable=False)
    height_cm   = Column(Float,   nullable=False)
    age         = Column(Integer, nullable=False)
    routine     = Column(String,  nullable=False)
    goal        = Column(String,  nullable=False)
    created_at  = Column(DateTime, nullable=False)
    weekly_plan = Column(Text,    nullable=False, default="[]")