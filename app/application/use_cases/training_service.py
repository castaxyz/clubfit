from app.application.ports.input.training_use_case import TrainingUseCase
from app.application.ports.out.training_repository import TrainingRepositoryPort
from app.domain.model.training_plan import TrainingPlan
# ↓ antes importaba Routine y Goal desde training_plan, ahora desde value_objects
from app.domain.model.value_objects import Routine, Goal


class TrainingService(TrainingUseCase):

    def __init__(self, repository: TrainingRepositoryPort):
        self.repository = repository

    def generate_plan(self, member_id, member_name, weight_kg,
                        height_cm, age, routine, goal) -> dict:
        try:
            routine_enum = Routine(routine)
            goal_enum    = Goal(goal)
        except ValueError as e:
            raise ValueError(f"Valor inválido: {e}")

        plan = TrainingPlan(
            member_id=member_id,   member_name=member_name,
            weight_kg=weight_kg,   height_cm=height_cm,
            age=age,               routine=routine_enum,
            goal=goal_enum,
        )
        plan.generate_weekly_plan()
        saved = self.repository.save(plan)
        return saved.to_summary()

    def get_plan(self, plan_id: int) -> dict:
        plan = self.repository.get_by_id(plan_id)
        if not plan:
            raise ValueError(f"Plan {plan_id} no encontrado")
        return plan.to_summary()

    def list_plans_by_member(self, member_id: int) -> list:
        return [p.to_summary() for p in self.repository.list_by_member(member_id)]

    def delete_plan(self, plan_id: int) -> None:
        if not self.repository.get_by_id(plan_id):
            raise ValueError(f"Plan {plan_id} no encontrado")
        self.repository.delete(plan_id)