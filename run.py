from flask import Flask

from app.application.use_cases.member_service import MemberService
from app.application.use_cases.training_service import TrainingService
from app.infrastructure.adapters.output.persistence.member_repository_sqlalchemy import MemberRepositorySQLAlchemy
from app.infrastructure.adapters.output.persistence.training_repository_sqlalchemy import TrainingRepositorySQLAlchemy
from app.infrastructure.adapters.output.messaging.redis_publisher import RedisPublisher
from app.infrastructure.adapters.input.member_controller import create_routes
from app.infrastructure.adapters.input.training_controller import create_training_routes
from app.infrastructure.adapters.output.persistence.member_entity import Base as MemberBase
from app.infrastructure.adapters.output.persistence.training_entity import Base as TrainingBase
from app.infrastructure.adapters.output.persistence.database import engine


def create_app():
    app = Flask(__name__)

    # Crear tablas de ambos dominios
    MemberBase.metadata.create_all(engine)
    TrainingBase.metadata.create_all(engine)

    # Microservicio 1: Miembros
    member_repository = MemberRepositorySQLAlchemy()
    publisher         = RedisPublisher()
    member_use_cases  = MemberService(member_repository, publisher)
    app.register_blueprint(create_routes(member_use_cases))

    # Microservicio 2: Planes de entrenamiento
    training_repository = TrainingRepositorySQLAlchemy()
    training_use_cases  = TrainingService(training_repository)
    app.register_blueprint(create_training_routes(training_use_cases))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
