from flask import Blueprint, request, jsonify
from datetime import datetime

from app.domain.entities.member import Member

member_bp = Blueprint("members", __name__)


def create_routes(use_cases):

    @member_bp.route("/")
    def home():
        return {"message": "ClubFit API running"}

    @member_bp.route("/members", methods=["POST"])
    def create_member():

        data = request.json

        member = Member(
            id=data["id"],
            name=data["name"],
            join_date=datetime.now(),
            expiration_date=datetime.now(),
        )

        use_cases.create_member(member)

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