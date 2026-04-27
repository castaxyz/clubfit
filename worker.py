import logging
import signal
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("expiry-worker")

from app.infrastructure.adapters.output.persistence.expiry_repository_sqlalchemy import ExpiryRepositorySQLAlchemy
from app.infrastructure.adapters.output.messaging.redis_publisher import RedisPublisher
from app.application.use_cases.expiry_service import ExpiryService
from app.infrastructure.adapters.input.redis_subscriber import RedisSubscriber
from app.infrastructure.scheduler.expiry_scheduler import ExpiryScheduler


def main():

    repository = ExpiryRepositorySQLAlchemy()
    publisher  = RedisPublisher()
    service    = ExpiryService(repository, publisher)

    scheduler  = ExpiryScheduler(publisher)
    scheduler.start()

    subscriber = RedisSubscriber(service)

    def shutdown(sig, frame):
        scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)

    logger.info("Corriendo batch inicial...")
    result = service.run_expiry_batch()
    logger.info("Batch inicial: %s", result)

    subscriber.start_listening()


if __name__ == "__main__":
    main()