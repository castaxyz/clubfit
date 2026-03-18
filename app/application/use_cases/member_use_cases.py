from app.domain.entities.member import Member


class MemberUseCases:

    def __init__(self, member_repository):
        self.member_repository = member_repository

    def create_member(self, id, name, join_date=None):
        member = Member.create_new(id, name, join_date)
        return self.member_repository.save(member)

    def list_members(self):
        return self.member_repository.list_all()

    def get_member(self, member_id):
        return self.member_repository.get_by_id(member_id)

    def delete_member(self, member_id):
        return self.member_repository.delete(member_id)

    def update_member(self, member_id, name):
        member = self.member_repository.get_by_id(member_id)
        if not member:
            raise Exception("Member not found")
        
        member.name = name
        return self.member_repository.save(member)

    def renew_membership(self, member_id):

        member = self.member_repository.get_by_id(member_id)

        if not member:
            raise Exception("Member not found")

        member.renew_membership()

        self.member_repository.save(member)

        return member