from app.domain.services.plan_strategy import PlanStrategy
from app.domain.model.value_objects import IMCCategory

class LoseWeightStrategy(PlanStrategy):
    def focuses(self):
        return ["HIIT + Full Body","Tren Superior","Cardio + Core","Tren Inferior","Full Body Circuito","Movilidad + Yoga"]

    def cardio_minutes(self, imc: IMCCategory) -> int:
        return 45 if imc in (IMCCategory.OVERWEIGHT, IMCCategory.OBESE) else 30