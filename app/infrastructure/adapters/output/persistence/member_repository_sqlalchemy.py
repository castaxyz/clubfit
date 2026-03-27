from app.application.ports.out.member_repository import MemberRepositoryPort
from app.infrastructure.adapters.mappers.member_mapper import MemberMapper
from app.infrastructure.adapters.output.persistence.database import SessionLocal
from app.infrastructure.adapters.output.persistence.member_entity import MemberEntity


class MemberRepositorySQLAlchemy(MemberRepositoryPort):

    def save(self, member):
        session = SessionLocal()
        model = session.get(MemberEntity, member.id)

        if not model:
            model = MemberMapper.to_entity(member)
            session.add(model)
        else:
            MemberMapper.update_model(model, member)

        session.commit()
        session.close()
        return member

    def get_by_id(self, member_id):
        session = SessionLocal()
        model = session.get(MemberEntity, member_id)
        session.close()
        return MemberMapper.to_domain(model) if model else None

    def get_by_email(self, email):
        session = SessionLocal()
        model = session.query(MemberEntity).filter_by(email=email).first()
        session.close()
        return MemberMapper.to_domain(model) if model else None

    def list_all(self):
        session = SessionLocal()
        models = session.query(MemberEntity).all()
        session.close()
        return [MemberMapper.to_domain(m) for m in models]

    def delete(self, member_id):
        session = SessionLocal()
        model = session.get(MemberEntity, member_id)
        if model:
            session.delete(model)
            session.commit()
        session.close()