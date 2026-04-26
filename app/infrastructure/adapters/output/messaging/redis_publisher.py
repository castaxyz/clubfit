import json
import os

import redis

from app.application.ports.out.event_publisher import EventPublisherPort


class RedisPublisher(EventPublisherPort):

    def __init__(self):
        self._client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )

    def publish(self, channel: str, message: dict) -> None:
        self._client.publish(channel, json.dumps(message))