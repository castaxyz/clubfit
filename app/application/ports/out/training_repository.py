from abc import ABC, abstractmethod
from typing import List, Optional


class TrainingRepositoryPort(ABC):

    @abstractmethod
    def save(self, plan) -> object:
        pass

    @abstractmethod
    def get_by_id(self, plan_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def list_by_member(self, member_id: int) -> List[object]:
        pass

    @abstractmethod
    def delete(self, plan_id: int) -> None:
        pass