from flask import Blueprint, request, jsonify
from datetime import datetime

member_bp = Blueprint("members", __name__)


def create_routes(use_cases):

    @member_bp.route("/")
    def home():
        return {"message": "ClubFit API running"}

    @member_bp.route("/members", methods=["POST"])
    def create_member():

        data = request.json

        required = ["id", "name", "email", "phone"]
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({"error": f"Campos obligatorios faltantes: {missing}"}), 400
        
        # Opcional: Para migración de datos antiguos (Prueba de negocio)
        join_date_str = data.get("join_date")
        join_date = datetime.fromisoformat(join_date_str) if join_date_str else None

        try:
            member = use_cases.create_member(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                join_date=join_date,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 409
        
        return jsonify({
            "message": "Miembro creado exitosamente",
            "data": _member_to_dict(member),
        }), 201

    @member_bp.route("/members", methods=["GET"])
    def list_members():

        members = use_cases.list_members()

        result = []

        for m in members:
            result.append(
                {
                    "id": m.id,
                    "name": m.name,
                    "email": m.email, 
                    "phone": m.phone,
                    "join_date": str(m.join_date),
                    "expiration_date": str(m.expiration_date),
                    "status": m.status,
                    "last_benefit": m.last_benefit,
                    "renewal_count": m.renewal_count,
                }
            )

        return jsonify(result)

    @member_bp.route("/members/<int:member_id>", methods=["GET"])
    def get_member(member_id):
        member = use_cases.get_member(member_id)
        if not member:
            return jsonify({"error": "Member not found"}), 404
        
        return jsonify({
            "id": member.id,
            "name": member.name,
            "email": member.email,
            "phone": member.phone,
            "join_date": str(member.join_date),
            "expiration_date": str(member.expiration_date),
            "status": member.status,
            "last_benefit": member.last_benefit,
            "renewal_count": member.renewal_count,
        })

    @member_bp.route("/members/<int:member_id>", methods=["DELETE"])
    def delete_member(member_id):
        try:
            use_cases.delete_member(member_id)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
        return jsonify({"message": "Miembro eliminado"}), 200

    @member_bp.route("/members/<int:member_id>", methods=["PUT"])
    def update_member(member_id):
        data = request.json
        
        try:
            member = use_cases.update_member(
                member_id,
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone"),
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
 
        return jsonify({
            "message": "Miembro actualizado",
            "data": _member_to_dict(member),
        }), 200

    @member_bp.route("/members/<int:member_id>/renew", methods=["POST"])
    def renew(member_id):
        try:
            member, detail = use_cases.renew_membership(member_id)
        except ValueError as e:
            return jsonify({"error": str(e)}), 404
 
        bonus_applied = detail["benefit_applied"] == "MES_BONIFICADO"
 
        return jsonify({
            "message": (
                f"¡Membresía renovada con MES_BONIFICADO! ({detail['bonus_days_added']} días extra)"
                if bonus_applied
                else "Membresía renovada por 30 días (sin bono)"
            ),
            "data": _member_to_dict(member),
            "renewal_detail": {
                "benefit_applied": detail["benefit_applied"],
                "bonus_days_added": detail["bonus_days_added"],
                "new_expiration": str(detail["new_expiration"]),
                "months_as_member": detail["months_as_member"],
                "renewal_count": detail["renewal_count"],
                "eligible_for_bonus": bonus_applied,
            },
        }), 200

    return member_bp

def _member_to_dict(member):
    today = datetime.now()
    months = (today - member.join_date).days / 30.44
    return {
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "phone": member.phone,
        "join_date": str(member.join_date),
        "expiration_date": str(member.expiration_date),
        "status": member.status,
        "last_benefit": member.last_benefit,
        "renewal_count": member.renewal_count,
        "months_as_member": round(months, 1),
        "eligible_for_bonus": months > 12,
    }