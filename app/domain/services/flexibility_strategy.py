from app.domain.services.plan_strategy import PlanStrategy
from app.domain.model.value_objects import IMCCategory

class FlexibilityStrategy(PlanStrategy):
    def focuses(self):
        return ["Movilidad + Yoga","Core y Movilidad","Movilidad + Yoga","Core y Movilidad"]

    def cardio_minutes(self, imc: IMCCategory) -> int:
        return 0