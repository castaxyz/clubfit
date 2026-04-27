from app.domain.services.plan_strategy import PlanStrategy
from app.domain.model.value_objects import IMCCategory

class MaintainStrategy(PlanStrategy):
    def focuses(self):
        return ["Full Body","Cardio Intervalos","Hombros y Core","Piernas","Full Body"]

    def cardio_minutes(self, imc: IMCCategory) -> int:
        return 20 if imc in (IMCCategory.OVERWEIGHT, IMCCategory.OBESE) else 0