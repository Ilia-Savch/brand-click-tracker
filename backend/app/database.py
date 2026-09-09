import os
from collections.abc import Iterator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base


# Ищем .env относительно файла, а не текущей папки.
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def create_database_engine() -> Engine:
    database_url: str | URL | None = os.getenv("DATABASE_URL")

    if os.getenv("DATABASE_HOST"):
        database_url = URL.create(
            "postgresql+psycopg",
            username=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"],
            host=os.environ["DATABASE_HOST"],
            port=5432,
            database=os.environ["POSTGRES_DB"],
        )

    if not database_url:
        raise RuntimeError("Не задана переменная DATABASE_URL")

    return create_engine(
        database_url,
        pool_pre_ping=True,
        connect_args={"connect_timeout": 5},
    )


engine: Engine = create_database_engine()

SessionFactory: sessionmaker[Session] = sessionmaker(bind=engine)


def init_database() -> None:
    Base.metadata.create_all(bind=engine)


def get_session() -> Iterator[Session]:
    with SessionFactory() as session:
        yield session
