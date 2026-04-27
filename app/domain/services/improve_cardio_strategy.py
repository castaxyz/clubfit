from app.domain.services.plan_strategy import PlanStrategy
from app.domain.model.value_objects import IMCCategory

class ImproveCardioStrategy(PlanStrategy):
    def focuses(self):
        return ["Cardio Intervalos","Full Body Funcional","Cardio Intervalos","Core y Movilidad","HIIT + Full Body","Movilidad + Yoga"]

    def cardio_minutes(self, imc: IMCCategory) -> int:
        return 45 if imc in (IMCCategory.OVERWEIGHT, IMCCategory.OBESE) else 40