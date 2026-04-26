from flask import Flask

from app.application.use_cases.member_service import MemberService
from app.infrastructure.adapters.output.persistence.member_repository_sqlalchemy import MemberRepositorySQLAlchemy
from app.infrastructure.adapters.output.messaging.redis_publisher import RedisPublisher  # ← NUEVO
from app.infrastructure.adapters.input.member_controller import create_routes
from app.infrastructure.adapters.output.persistence.member_entity import Base
from app.infrastructure.adapters.output.persistence.database import engine


def create_app():
    app = Flask(__name__)
    Base.metadata.create_all(engine)

    repository = MemberRepositorySQLAlchemy()
    publisher  = RedisPublisher()          # ← NUEVO: instanciar el publisher
    use_cases  = MemberService(repository, publisher)  # ← NUEVO: inyectarlo

    member_routes = create_routes(use_cases)
    app.register_blueprint(member_routes)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)