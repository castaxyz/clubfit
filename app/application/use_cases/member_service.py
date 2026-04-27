from datetime import datetime
from app.application.ports.input.member_use_case import MemberUseCase
from app.application.ports.out.member_repository import MemberRepositoryPort
from app.domain.model.member import Member


class MemberService(MemberUseCase):

    def __init__(self, member_repository: MemberRepositoryPort, event_publisher=None):
        self.member_repository = member_repository
        self.event_publisher = event_publisher   # ← NUEVO: inyección del publisher

    def create_member(self, id, name, email, phone, join_date=None):
        existing = self.member_repository.get_by_email(email)
        if existing:
            raise ValueError(f"Ya existe un miembro registrado con el email: {email}")
        member = Member.create_new(id, name, email, phone, join_date)
        return self.member_repository.save(member)

    def list_members(self):
        return self.member_repository.list_all()

    def get_member(self, member_id):
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError("Member not found")
        return member

    def delete_member(self, member_id):
        self.get_member(member_id)
        return self.member_repository.delete(member_id)

    def update_member(self, member_id, name=None, email=None, phone=None):
        member = self.get_member(member_id)
        if email and email != member.email:
            existing = self.member_repository.get_by_email(email)
            if existing:
                raise ValueError(f"El email {email} ya está en uso por otro miembro")
        if name:
            member.name = name
        if email:
            member.email = email
        if phone:
            member.phone = phone
        return self.member_repository.save(member)

    def renew_membership(self, member_id):
        member = self.get_member(member_id)
        renewal_detail = member.renew_membership()
        self.member_repository.save(member)

        if self.event_publisher:
            try:
                self.event_publisher.publish("membership.events", {
                    "event": "MEMBERSHIP_RENEWED",
                    "member_id": member_id,
                    "new_status": member.status,
                    "new_expiration": str(member.expiration_date),
                    "benefit": renewal_detail["benefit_applied"],
                    "timestamp": str(datetime.now()),
                })
            except Exception:
                pass

        return member, renewal_detail

    def trigger_expiry_check(self):
        if self.event_publisher:
            self.event_publisher.publish("membership.commands", {
                "command": "CHECK_EXPIRED_MEMBERSHIPS",
                "timestamp": str(datetime.now()),
            })
        return {"message": "Expiry check event published"}