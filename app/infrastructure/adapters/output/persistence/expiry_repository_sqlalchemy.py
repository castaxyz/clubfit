from datetime import datetime
from typing import List

from sqlalchemy import text

from app.application.ports.out.expiry_repository import ExpiryRepositoryPort
from app.infrastructure.adapters.output.persistence.database import SessionLocal


class ExpiryRepositorySQLAlchemy(ExpiryRepositoryPort):

    def find_expired_members(self) -> List[dict]:
        session = SessionLocal()
        try:
            rows = session.execute(
                text("""
                    SELECT id, name, email, expiration_date, status
                    FROM members
                    WHERE expiration_date < :now
                      AND status NOT IN ('EXPIRED')
                """),
                {"now": datetime.now()},
            ).fetchall()
            return [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
        finally:
            session.close()

    def bulk_mark_expired(self, member_ids: List[int]) -> int:
        if not member_ids:
            return 0
        session = SessionLocal()
        try:
            result = session.execute(
                text("""
                    UPDATE members
                    SET status = 'EXPIRED'
                    WHERE id IN :ids
                      AND status NOT IN ('EXPIRED')
                """),
                {"ids": tuple(member_ids)},
            )
            session.commit()
            return result.rowcount
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()