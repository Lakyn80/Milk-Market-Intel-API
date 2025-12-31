from app.db.base import Base
from app.db.session import engine

from app.modules.companies.models import Company  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("DB initialized successfully.")
