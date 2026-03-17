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
        
        # Opcional: Para migración de datos antiguos (Prueba de negocio)
        join_date_str = data.get("join_date")
        join_date = datetime.fromisoformat(join_date_str) if join_date_str else None

        use_cases.create_member(
            id=data["id"],
            name=data["name"],
            join_date=join_date
        )

        return jsonify({"message": "Member created"})


    @member_bp.route("/members", methods=["GET"])
    def list_members():

        members = use_cases.list_members()

        result = []

        for m in members:
            result.append(
                {
                    "id": m.id,
                    "name": m.name,
                    "expiration_date": str(m.expiration_date),
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
            "join_date": str(member.join_date),
            "expiration_date": str(member.expiration_date)
        })

    @member_bp.route("/members/<int:member_id>", methods=["DELETE"])
    def delete_member(member_id):
        use_cases.delete_member(member_id)
        return jsonify({"message": "Member deleted"})

    @member_bp.route("/members/<int:member_id>", methods=["PUT"])
    def update_member(member_id):
        data = request.json
        member = use_cases.update_member(member_id, data["name"])
        return jsonify({"message": "Member updated", "name": member.name})

    @member_bp.route("/members/<int:member_id>/renew", methods=["POST"])
    def renew(member_id):

        member = use_cases.renew_membership(member_id)

        return jsonify(
            {
                "message": "Membership renewed",
                "new_expiration": str(member.expiration_date),
            }
        )

    return member_bp