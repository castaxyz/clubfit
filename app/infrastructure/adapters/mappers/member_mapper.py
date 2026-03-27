from app.domain.model.member import MemberModel
from app.infrastructure.adapters.output.persistence.member_entity import MemberEntity


class MemberMapper:

    @staticmethod
    def to_domain(entity: MemberEntity) -> MemberModel:
        return MemberModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            phone=entity.phone,
            join_date=entity.join_date,
            expiration_date=entity.expiration_date,
            status=entity.status,
            last_benefit=entity.last_benefit,
            renewal_count=entity.renewal_count,
        )

    @staticmethod
    def to_entity(memberModel: MemberModel) -> MemberEntity:
        return MemberEntity(
            id=memberModel.id,
            name=memberModel.name,
            email=memberModel.email,
            phone=memberModel.phone,
            join_date=memberModel.join_date,
            expiration_date=memberModel.expiration_date,
            status=memberModel.status,
            last_benefit=memberModel.last_benefit,
            renewal_count=memberModel.renewal_count,
        )

    @staticmethod
    def update_model(entity: MemberEntity, memberModel: MemberModel) -> None:
        entity.name = memberModel.name
        entity.email = memberModel.email
        entity.phone = memberModel.phone
        entity.expiration_date = memberModel.expiration_date
        entity.status = memberModel.status
        entity.last_benefit = memberModel.last_benefit
        entity.renewal_count = memberModel.renewal_count