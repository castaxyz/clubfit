from typing import List
from app.domain.model.exercise import DayPlan
from app.domain.model.exercise_catalog import ExerciseCatalog
from app.domain.model.value_objects import Goal, Routine, IMCCategory
from app.domain.services.plan_strategy import PlanStrategy
from app.domain.services.lose_weight_strategy import LoseWeightStrategy
from app.domain.services.gain_muscle_strategy import GainMuscleStrategy
from app.domain.services.improve_cardio_strategy import ImproveCardioStrategy
from app.domain.services.flexibility_strategy import FlexibilityStrategy
from app.domain.services.maintain_strategy import MaintainStrategy

DAYS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

SESSIONS_BY_ROUTINE = {
    Routine.SEDENTARY:   2,
    Routine.LIGHT:       3,
    Routine.MODERATE:    4,
    Routine.ACTIVE:      5,
    Routine.VERY_ACTIVE: 6,
}


def resolve_strategy(goal: Goal) -> PlanStrategy:
    strategies = {
        Goal.LOSE_WEIGHT:    LoseWeightStrategy(),
        Goal.GAIN_MUSCLE:    GainMuscleStrategy(),
        Goal.IMPROVE_CARDIO: ImproveCardioStrategy(),
        Goal.FLEXIBILITY:    FlexibilityStrategy(),
        Goal.MAINTAIN:       MaintainStrategy(),
    }
    return strategies[goal]


class PlanGenerator:

    def __init__(self, goal: Goal, routine: Routine, imc_category: IMCCategory):
        self.strategy     = resolve_strategy(goal)
        self.sessions     = SESSIONS_BY_ROUTINE[routine]
        self.imc_category = imc_category

    def build(self) -> List[DayPlan]:
        focuses = self.strategy.focuses()
        return [
            DayPlan(
                day           = DAYS[i],
                focus         = focuses[i % len(focuses)],
                cardio_minutes= self.strategy.cardio_minutes(self.imc_category),
                exercises     = tuple(ExerciseCatalog.get(
                    focuses[i % len(focuses)], self.imc_category
                )),
            )
            for i in range(self.sessions)
        ]