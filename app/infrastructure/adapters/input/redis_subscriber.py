import json
import logging
import os
import redis

logger = logging.getLogger(__name__)


class RedisSubscriber:

    def __init__(self, expiry_use_case):
        self.expiry_use_case = expiry_use_case
        self._client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )

    def start_listening(self):
        pubsub = self._client.pubsub()
        pubsub.subscribe("membership.commands")
        logger.info("Escuchando canal 'membership.commands'...")

        for raw in pubsub.listen():
            if raw["type"] != "message":
                continue
            try:
                payload = json.loads(raw["data"])
                if payload.get("command") == "CHECK_EXPIRED_MEMBERSHIPS":
                    result = self.expiry_use_case.run_expiry_batch()
                    logger.info("Batch result: %s", result)
            except Exception as e:
                logger.error("Error procesando comando: %s", e)