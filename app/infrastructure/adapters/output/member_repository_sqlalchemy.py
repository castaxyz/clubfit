from app.domain.ports.member_repository import MemberRepository
from app.domain.entities.member import Member
from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.models import MemberModel


class MemberRepositorySQLAlchemy(MemberRepository):

    def save(self, member):

        session = SessionLocal()

        model = session.query(MemberModel).get(member.id)

        if not model:
            model = MemberModel(
                id=member.id,
                name=member.name,
                join_date=member.join_date,
                expiration_date=member.expiration_date,
            )
            session.add(model)
        else:
            model.expiration_date = member.expiration_date

        session.commit()
        session.close()

        return member

    def get_by_id(self, member_id):

        session = SessionLocal()

        model = session.query(MemberModel).get(member_id)

        session.close()

        if not model:
            return None

        return Member(
            model.id,
            model.name,
            model.join_date,
            model.expiration_date,
        )

    def list_all(self):

        session = SessionLocal()

        models = session.query(MemberModel).all()

        session.close()

        members = []

        for m in models:
            members.append(
                Member(
                    m.id,
                    m.name,
                    m.join_date,
                    m.expiration_date,
                )
            )

        return members

    def delete(self, member_id):
        session = SessionLocal()
        model = session.query(MemberModel).get(member_id)
        if model:
            session.delete(model)
            session.commit()
        session.close()