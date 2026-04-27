from flask import Blueprint, request, jsonify

training_bp = Blueprint("training", __name__)


def create_training_routes(use_cases):

    @training_bp.route("/training-plans/options", methods=["GET"])
    def options():
        return jsonify({
            "routines": ["SEDENTARY", "LIGHT", "MODERATE", "ACTIVE", "VERY_ACTIVE"],
            "goals":    ["LOSE_WEIGHT", "GAIN_MUSCLE", "MAINTAIN", "IMPROVE_CARDIO", "FLEXIBILITY"],
            "routine_descriptions": {
                "SEDENTARY":   "Poco o nada de ejercicio — 2 días/semana",
                "LIGHT":       "Ejercicio ligero 1-3 días/semana — 3 días/semana",
                "MODERATE":    "Ejercicio moderado 3-5 días/semana — 4 días/semana",
                "ACTIVE":      "Ejercicio intenso 6-7 días/semana — 5 días/semana",
                "VERY_ACTIVE": "Ejercicio muy intenso o trabajo físico — 6 días/semana",
            },
            "goal_descriptions": {
                "LOSE_WEIGHT":    "Déficit -400 kcal + cardio prioritario",
                "GAIN_MUSCLE":    "Superávit +300 kcal + énfasis en fuerza",
                "MAINTAIN":       "Calorías de mantenimiento + balance fuerza/cardio",
                "IMPROVE_CARDIO": "Cardio 40+ min + HIIT + resistencia",
                "FLEXIBILITY":    "Yoga, movilidad y recuperación activa",
            },
        })

    @training_bp.route("/training-plans", methods=["POST"])
    def generate_plan():
        data     = request.json or {}
        required = ["member_id", "member_name", "weight_kg", "height_cm", "age", "routine", "goal"]
        missing  = [f for f in required if f not in data]
        if missing:
            return jsonify({"error": f"Campos obligatorios faltantes: {missing}"}), 400
        try:
            plan = use_cases.generate_plan(
                member_id=int(data["member_id"]),
                member_name=str(data["member_name"]),
                weight_kg=float(data["weight_kg"]),
                height_cm=float(data["height_cm"]),
                age=int(data["age"]),
                routine=str(data["routine"]),
                goal=str(data["goal"]),
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify({"message": "Plan de entrenamiento generado exitosamente", "data": plan}), 201

    @training_bp.route("/training-plans/<int:plan_id>", methods=["GET"])
    def get_plan(plan_id):
        try:
            return jsonify(use_cases.get_plan(plan_id))
        except ValueError as e:
            return jsonify({"error": str(e)}), 404

    @training_bp.route("/training-plans/member/<int:member_id>", methods=["GET"])
    def list_by_member(member_id):
        plans = use_cases.list_plans_by_member(member_id)
        return jsonify({"member_id": member_id, "total": len(plans), "plans": plans})

    @training_bp.route("/training-plans/<int:plan_id>", methods=["DELETE"])
    def delete_plan(plan_id):
        try:
            use_cases.delete_plan(plan_id)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        return jsonify({"message": f"Plan {plan_id} eliminado"}), 200

    return training_bp
