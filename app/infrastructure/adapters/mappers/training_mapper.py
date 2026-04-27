import json
from app.domain.model.training_plan import TrainingPlan
from app.domain.model.exercise import DayPlan, Exercise
from app.domain.model.value_objects import Routine, Goal
from app.infrastructure.adapters.output.persistence.training_entity import TrainingPlanModel


class TrainingMapper:

    @staticmethod
    def to_model(plan: TrainingPlan) -> TrainingPlanModel:
        weekly_json = json.dumps([{
            "day": d.day,
            "focus": d.focus,
            "cardio_minutes": d.cardio_minutes,
            "exercises": [{
                "name": e.name, "sets": e.sets, "reps": e.reps,
                "rest_seconds": e.rest_seconds, "notes": e.notes,
            } for e in d.exercises],  # d.exercises ahora es tuple (frozen)
        } for d in plan.weekly_plan], ensure_ascii=False)

        return TrainingPlanModel(
            id=plan.id,           member_id=plan.member_id,
            member_name=plan.member_name,
            weight_kg=plan.weight_kg, height_cm=plan.height_cm, age=plan.age,
            routine=plan.routine.value, goal=plan.goal.value,
            created_at=plan.created_at, weekly_plan=weekly_json,
        )

    @staticmethod
    def to_domain(model: TrainingPlanModel) -> TrainingPlan:
        days = [
            DayPlan(
                day           = d["day"],
                focus         = d["focus"],
                cardio_minutes= d.get("cardio_minutes", 0),
                exercises     = tuple(  # reconstruir como tuple (frozen)
                    Exercise(
                        name=e["name"], sets=e["sets"], reps=e["reps"],
                        rest_seconds=e["rest_seconds"], notes=e.get("notes", "")
                    )
                    for e in d.get("exercises", [])
                ),
            )
            for d in json.loads(model.weekly_plan)
        ]
        return TrainingPlan(
            id=model.id,           member_id=model.member_id,
            member_name=model.member_name,
            weight_kg=model.weight_kg, height_cm=model.height_cm, age=model.age,
            routine=Routine(model.routine), goal=Goal(model.goal),
            created_at=model.created_at, weekly_plan=days,
        )