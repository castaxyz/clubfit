from abc import ABC, abstractmethod


class EventPublisherPort(ABC):

    @abstractmethod
    def publish(self, channel: str, message: dict) -> None:
        pass