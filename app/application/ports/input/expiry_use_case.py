from abc import ABC, abstractmethod


class ExpiryUseCase(ABC):

    @abstractmethod
    def run_expiry_batch(self) -> dict:
        pass