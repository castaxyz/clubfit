from typing import List
from app.domain.model.exercise import Exercise
from app.domain.model.value_objects import IMCCategory


class ExerciseCatalog:

    @staticmethod
    def get(focus: str, imc_category: IMCCategory) -> List[Exercise]:
        low_impact = imc_category == IMCCategory.OBESE
        catalog = ExerciseCatalog._build(low_impact)
        return catalog.get(focus, ExerciseCatalog._default())

    @staticmethod
    def _default() -> List[Exercise]:
        return [
            Exercise("Sentadilla", 3, "12", 60),
            Exercise("Press de banca", 3, "10", 75),
            Exercise("Plancha", 3, "30 seg", 30),
        ]

    @staticmethod
    def _build(low_impact: bool) -> dict:
        return {
            "Pecho y Tríceps": [
                Exercise("Press de banca", 4, "10-12", 90, "Control en la bajada"),
                Exercise("Aperturas con mancuernas", 3, "12", 60),
                Exercise("Fondos en paralelas", 3, "hasta el fallo", 90),
                Exercise("Extensiones tríceps polea", 3, "15", 60),
            ],
            "Espalda y Bíceps": [
                Exercise("Jalón al pecho", 4, "10-12", 90),
                Exercise("Remo con barra", 4, "10", 90, "Espalda recta"),
                Exercise("Curl de bíceps", 3, "12", 60),
                Exercise("Face pulls", 3, "15", 60, "Para manguito rotador"),
            ],
            "Piernas": [
                Exercise("Prensa de pierna" if low_impact else "Sentadilla libre", 4, "10-12", 120),
                Exercise("Peso muerto rumano", 3, "12", 90, "Bisagra de cadera"),
                Exercise("Extensiones de cuádriceps", 3, "15", 60),
                Exercise("Curl femoral", 3, "15", 60),
                Exercise("Elevaciones de gemelos", 4, "20", 45),
            ],
            "Hombros y Core": [
                Exercise("Press militar", 4, "10-12", 90),
                Exercise("Elevaciones laterales", 3, "15", 60),
                Exercise("Plancha frontal", 3, "40 seg", 45),
                Exercise("Rueda abdominal", 3, "10", 60, "Controlado"),
            ],
            "HIIT + Full Body": [
                Exercise("Marcha en sitio" if low_impact else "Jumping Jacks", 4, "30 seg", 15),
                Exercise("Sentadillas lentas" if low_impact else "Sentadillas pliométricas", 4, "12", 30),
                Exercise("Plancha estática" if low_impact else "Mountain climbers", 3, "20 seg", 20),
                Exercise("Burpees modificados", 3, "8", 45),
            ],
            "Cardio Intervalos": [
                Exercise("Trote intervalado", 6, "1 ciclo", 120, "1min rápido / 2min moderado"),
                Exercise("Bicicleta estática sprints", 4, "30 seg", 90),
                Exercise("Step rápido" if low_impact else "Cuerda de saltar", 3, "1 min", 60),
            ],
            "Core y Movilidad": [
                Exercise("Plancha frontal", 4, "45 seg", 30),
                Exercise("Plancha lateral", 3, "30 seg c/lado", 30),
                Exercise("Dead bug", 3, "10 c/lado", 45),
                Exercise("Estiramientos de cadera", 2, "60 seg", 0, "Mantenido"),
            ],
            "Movilidad + Yoga": [
                Exercise("Saludo al sol", 3, "5 rondas", 0),
                Exercise("Postura del guerrero", 2, "60 seg c/lado", 0),
                Exercise("Paloma (cadera)", 2, "90 seg c/lado", 0),
                Exercise("Foam roll", 1, "10 min", 0),
            ],
        }