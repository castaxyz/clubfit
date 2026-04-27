from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class Exercise:
    name:         str
    sets:         int
    reps:         str
    rest_seconds: int
    notes:        str = ""

@dataclass(frozen=True)
class DayPlan:
    day:            str
    focus:          str
    cardio_minutes: int
    exercises:      tuple