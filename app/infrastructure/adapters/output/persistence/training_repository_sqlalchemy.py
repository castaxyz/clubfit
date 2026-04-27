from typing import List, Optional
from app.application.ports.out.training_repository import TrainingRepositoryPort
from app.domain.model.training_plan import TrainingPlan
from app.infrastructure.adapters.output.persistence.database import SessionLocal
from app.infrastructure.adapters.output.persistence.training_entity import TrainingPlanModel
from app.infrastructure.adapters.mappers.training_mapper import TrainingMapper

class TrainingRepositorySQLAlchemy(TrainingRepositoryPort):

    def save(self, plan: TrainingPlan) -> TrainingPlan:
        session = SessionLocal()
        model   = TrainingMapper.to_model(plan)
        session.add(model)
        session.commit()
        session.refresh(model)
        result  = TrainingMapper.to_domain(model)
        session.close()
        return result

    def get_by_id(self, plan_id: int) -> Optional[TrainingPlan]:
        session = SessionLocal()
        model   = session.get(TrainingPlanModel, plan_id)
        session.close()
        return TrainingMapper.to_domain(model) if model else None

    def list_by_member(self, member_id: int) -> List[TrainingPlan]:
        session = SessionLocal()
        models  = session.query(TrainingPlanModel).filter_by(member_id=member_id).all()
        session.close()
        return [TrainingMapper.to_domain(m) for m in models]

    def delete(self, plan_id: int) -> None:
        session = SessionLocal()
        model   = session.get(TrainingPlanModel, plan_id)
        if model:
            session.delete(model)
            session.commit()
        session.close()