from flask import Flask

from app.application.use_cases.member_use_cases import MemberUseCases
from app.infrastructure.adapters.output.member_repository_sqlalchemy import (
    MemberRepositorySQLAlchemy,
)
from app.infrastructure.adapters.input.member_controller import create_routes
from app.infrastructure.persistence.models import Base
from app.infrastructure.persistence.database import engine


def create_app():

    app = Flask(__name__)

    Base.metadata.create_all(engine)

    repository = MemberRepositorySQLAlchemy()

    use_cases = MemberUseCases(repository)

    member_routes = create_routes(use_cases)

    app.register_blueprint(member_routes)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)