import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from config import DB_PORT_TEST, DB_USER_TEST, DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST
from ...database.database import Base, get_db
from ...main import app
from fastapi.testclient import TestClient

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

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def create_menu(client):
    menu_data = {'title': 'Тестовое меню', 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def create_submenu(client, create_menu):
    submenu_data = {'title': 'Тестовое подменю', 'description': 'Тестовое подменю'}
    response = client.post(f"/api/v1/menus/{create_menu['id']}/submenus", json=submenu_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def create_dish(client, create_menu, create_submenu):
    dish_data = {'title': 'Тестовое блюдо', 'description': 'Тестовое описание блюда', 'price': 12.50}
    response = client.post(f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes", json=dish_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()



