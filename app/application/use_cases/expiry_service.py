from datetime import datetime

from app.application.ports.input.expiry_use_case import ExpiryUseCase
from app.application.ports.out.expiry_repository import ExpiryRepositoryPort
from app.application.ports.out.event_publisher import EventPublisherPort
from app.domain.model.expiry_batch_result import ExpiryBatchResult


class ExpiryService(ExpiryUseCase):

    def __init__(self, repository: ExpiryRepositoryPort, publisher: EventPublisherPort = None):
        self.repository = repository
        self.publisher   = publisher

    def run_expiry_batch(self) -> dict:
        now             = datetime.now()
        expired_members = self.repository.find_expired_members()

        result = ExpiryBatchResult(
            processed_at=now,
            total_expired=len(expired_members),
        )

        if not expired_members:
            return self._to_dict(result)

        ids = [m["id"] for m in expired_members]

        try:
            count             = self.repository.bulk_mark_expired(ids)
            result.updated_ids = ids[:count]
        except Exception as e:
            result.errors.append(str(e))
            return self._to_dict(result)

        # Publicar evento (fire-and-forget)
        if self.publisher and result.updated_ids:
            try:
                self.publisher.publish("membership.events", {
                    "event":       "MEMBERSHIPS_EXPIRED",
                    "expired_ids":  result.updated_ids,
                    "total":        len(result.updated_ids),
                    "processed_at": str(now),
                })
            except Exception:
                pass

        return self._to_dict(result)

    def _to_dict(self, result: ExpiryBatchResult) -> dict:
        return {
            "processed_at":  str(result.processed_at),
            "total_expired":  result.total_expired,
            "updated_ids":    result.updated_ids,
            "success":        result.success,
            "errors":         result.errors,
        }