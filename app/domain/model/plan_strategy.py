from abc import ABC, abstractmethod
from typing import List
from app.domain.model.exercise import DayPlan
from app.domain.model.value_objects import IMCCategory

class PlanStrategy(ABC):

    @abstractmethod
    def focuses(self) -> List[str]:
        pass

    @abstractmethod
    def cardio_minutes(self, imc: IMCCategory) -> int:
        pass