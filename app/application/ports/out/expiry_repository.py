from abc import ABC, abstractmethod
from typing import List


class ExpiryRepositoryPort(ABC):

    @abstractmethod
    def find_expired_members(self) -> List[dict]:
        pass

    @abstractmethod
    def bulk_mark_expired(self, member_ids: List[int]) -> int:
        pass