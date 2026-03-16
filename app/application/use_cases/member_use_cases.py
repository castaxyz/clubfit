class MemberUseCases:

    def __init__(self, member_repository):
        self.member_repository = member_repository

    def create_member(self, member):
        return self.member_repository.save(member)

    def list_members(self):
        return self.member_repository.list_all()

    def renew_membership(self, member_id):

        member = self.member_repository.get_by_id(member_id)

        if not member:
            raise Exception("Member not found")

        member.renew_membership()

        self.member_repository.save(member)

        return member