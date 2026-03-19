from app.domain.entities.member import Member


class MemberUseCases:

    def __init__(self, member_repository):
        self.member_repository = member_repository

    def create_member(self, id, name, email, phone, join_date=None):
        existing = self.member_repository.get_by_email(email)
        if existing:
            raise ValueError(f"Ya existe un miembro registrado con el email: {email}")
        
        member = Member.create_new(id, name, email, phone, join_date)
        return self.member_repository.save(member)

    def list_members(self):
        return self.member_repository.list_all()

    def get_member(self, member_id):
        return self.member_repository.get_by_id(member_id)

    def delete_member(self, member_id):
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError("Miembro no encontrado")
        return self.member_repository.delete(member_id)

    def update_member(self, member_id, name=None, email=None, phone=None):
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise ValueError("Member not found")
        
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

        member = self.member_repository.get_by_id(member_id)

        if not member:
            raise ValueError("Member not found")

        renewal_detail = member.renew_membership()
        self.member_repository.save(member)

        return member, renewal_detail