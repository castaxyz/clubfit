from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from app.domain.model.value_objects import Routine, Goal, IMCCategory
from app.domain.model.exercise import DayPlan
from app.domain.services.plan_generator import PlanGenerator

ACTIVITY_FACTORS = {
    Routine.SEDENTARY:   1.2,   Routine.LIGHT:       1.375,
    Routine.MODERATE:    1.55,  Routine.ACTIVE:      1.725,
    Routine.VERY_ACTIVE: 1.9,
}

@dataclass
class TrainingPlan:
    member_id:   int
    member_name: str
    weight_kg:   float
    height_cm:   float
    age:         int
    routine:     Routine
    goal:        Goal
    created_at:  datetime     = field(default_factory=datetime.now)
    weekly_plan: List[DayPlan] = field(default_factory=list)
    id:          Optional[int]  = None

    @property
    def imc(self) -> float:
        return round(self.weight_kg / ((self.height_cm / 100) ** 2), 2)

    @property
    def imc_category(self) -> IMCCategory:
        if self.imc < 18.5:  return IMCCategory.UNDERWEIGHT
        if self.imc < 25:    return IMCCategory.NORMAL
        if self.imc < 30:    return IMCCategory.OVERWEIGHT
        return IMCCategory.OBESE

    @property
    def daily_calories(self) -> int:
        bmr  = 10*self.weight_kg + 6.25*self.height_cm - 5*self.age + 5
        base = bmr * ACTIVITY_FACTORS[self.routine]
        if self.goal == Goal.LOSE_WEIGHT:  return int(base - 400)
        if self.goal == Goal.GAIN_MUSCLE:   return int(base + 300)
        return int(base)

    def generate_weekly_plan(self) -> None:
        self.weekly_plan = PlanGenerator(
            self.goal, self.routine, self.imc_category
        ).build()
    def to_summary(self) -> dict:
        return {
            "id":             self.id,
            "member_id":      self.member_id,
            "member_name":    self.member_name,
            "weight_kg":      self.weight_kg,
            "height_cm":      self.height_cm,
            "age":            self.age,
            "imc":            self.imc,
            "imc_category":   self.imc_category.value,
            "routine":        self.routine.value,
            "goal":           self.goal.value,
            "daily_calories": self.daily_calories,
            "created_at":     str(self.created_at),
            "weekly_plan": [{
                "day":            d.day,
                "focus":          d.focus,
                "cardio_minutes": d.cardio_minutes,
                "exercises": [{
                    "name":         e.name,
                    "sets":         e.sets,
                    "reps":         e.reps,
                    "rest_seconds": e.rest_seconds,
                    "notes":        e.notes,
                } for e in d.exercises],
            } for d in self.weekly_plan],
        }
