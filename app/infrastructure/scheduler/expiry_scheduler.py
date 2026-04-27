import logging
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


class ExpiryScheduler:

    def __init__(self, publisher):
        self.publisher = publisher
        interval     = int(os.getenv("EXPIRY_CHECK_INTERVAL_MINUTES", 60))
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_job(
            func=self._dispatch,
            trigger="interval",
            minutes=interval,
            id="expiry_check_job",
            replace_existing=True,
        )

    def _dispatch(self):
        # Publica el comando y retorna inmediatamente
        try:
            self.publisher.publish("membership.commands", {
                "command":   "CHECK_EXPIRED_MEMBERSHIPS",
                "source":    "scheduler",
                "timestamp": str(datetime.now()),
            })
        except Exception as e:
            logger.error("Scheduler dispatch error: %s", e)

    def start(self):
        self._scheduler.start()

    def shutdown(self):
        self._scheduler.shutdown()