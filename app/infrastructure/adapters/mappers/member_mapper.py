from app.domain.model.member import Member
from app.infrastructure.adapters.output.persistence.member_entity import MemberModel


class MemberMapper:

    @staticmethod
    def to_domain(model: MemberModel) -> Member:
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

    @staticmethod
    def to_model(member: Member) -> MemberModel:
        return MemberModel(
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

    @staticmethod
    def update_model(model: MemberModel, member: Member) -> None:
        model.name = member.name
        model.email = member.email
        model.phone = member.phone
        model.expiration_date = member.expiration_date
        model.status = member.status
        model.last_benefit = member.last_benefit
        model.renewal_count = member.renewal_count