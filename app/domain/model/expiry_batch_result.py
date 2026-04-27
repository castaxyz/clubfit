from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class ExpiryBatchResult:
    processed_at: datetime
    total_expired: int
    updated_ids: List[int] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0