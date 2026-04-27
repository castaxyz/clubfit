from app.domain.services.plan_strategy import PlanStrategy
from app.domain.model.value_objects import IMCCategory

class GainMuscleStrategy(PlanStrategy):
    def focuses(self):
        return ["Pecho y Tríceps","Espalda y Bíceps","Piernas","Hombros y Core","Full Body","Espalda y Bíceps"]

    def cardio_minutes(self, imc: IMCCategory) -> int:
        return 0