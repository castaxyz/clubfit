from abc import ABC, abstractmethod


class TrainingUseCase(ABC):

    @abstractmethod
    def generate_plan(self, member_id: int, member_name: str,
                          weight_kg: float, height_cm: float,
                          age: int, routine: str, goal: str) -> dict:
        pass

    @abstractmethod
    def get_plan(self, plan_id: int) -> dict:
        pass

    @abstractmethod
    def list_plans_by_member(self, member_id: int) -> list:
        pass

    @abstractmethod
    def delete_plan(self, plan_id: int) -> None:
        pass