from abc import ABC, abstractmethod


class MemberUseCase(ABC):

    @abstractmethod
    def create_member(self, id, name, email, phone, join_date=None):
        pass

    @abstractmethod
    def list_members(self):
        pass

    @abstractmethod
    def get_member(self, member_id):
        pass

    @abstractmethod
    def update_member(self, member_id, name=None, email=None, phone=None):
        pass

    @abstractmethod
    def delete_member(self, member_id):
        pass

    @abstractmethod
    def renew_membership(self, member_id):
        pass