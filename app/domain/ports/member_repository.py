from abc import ABC, abstractmethod


class MemberRepository(ABC):

    @abstractmethod
    def save(self, member):
        pass

    @abstractmethod
    def get_by_id(self, member_id):
        pass

    @abstractmethod
    def get_by_email(self, email):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def delete(self, member_id):
        pass