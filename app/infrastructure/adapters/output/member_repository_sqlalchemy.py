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
                email=member.email,
                phone=member.phone,
                join_date=member.join_date,
                expiration_date=member.expiration_date,
                status=member.status,
                last_benefit=member.last_benefit,
                renewal_count=member.renewal_count,
            )
            session.add(model)
        else:
            model.name = member.name
            model.email = member.email
            model.phone = member.phone
            model.expiration_date = member.expiration_date
            model.status = member.status
            model.last_benefit = member.last_benefit
            model.renewal_count = member.renewal_count

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
            id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            join_date=model.join_date,
            expiration_date=model.expiration_date,
            status=model.status,
            last_benefit=model.last_benefit,
            renewal_count=model.renewal_count,
        )

    def get_by_email(self, email):
        session = SessionLocal()
        model = session.query(MemberModel).filter_by(email=email).first()
        session.close()
 
        if not model:
            return None
 
        return Member(
            id=model.id,
            name=model.name,
            email=model.email,
            phone=model.phone,
            join_date=model.join_date,
            expiration_date=model.expiration_date,
            status=model.status,
            last_benefit=model.last_benefit,
            renewal_count=model.renewal_count,
        )

    def list_all(self):

        session = SessionLocal()

        models = session.query(MemberModel).all()

        session.close()

        return [
            Member(
                id=m.id,
                name=m.name,
                email=m.email,
                phone=m.phone,
                join_date=m.join_date,
                expiration_date=m.expiration_date,
                status=m.status,
                last_benefit=m.last_benefit,
                renewal_count=m.renewal_count,
            )
            for m in models
        ]

    def delete(self, member_id):
        session = SessionLocal()
        model = session.query(MemberModel).get(member_id)
        if model:
            session.delete(model)
            session.commit()
        session.close()