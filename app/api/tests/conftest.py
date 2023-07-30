import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DB_PORT_TEST, DB_USER_TEST, DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST
from ...database.database import Base, get_db
from ...main import app

DATABASE_URL = f"postgresql://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

engine = create_engine(DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_cleanup():
    engine_clean = create_engine(DATABASE_URL)

    Base.metadata.create_all(engine_clean)

    cleaningSession = sessionmaker(autocommit=False, autoflush=False, bind=engine_clean)

    session = cleaningSession()

    try:
        for table in reversed(Base.metadata.sorted_tables):
            session.query(table).delete()

        session.commit()
    finally:
        session.close()


app.dependency_overrides[get_db] = override_get_db
