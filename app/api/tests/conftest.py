from __future__ import annotations

import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.api.models.models import Dish, Menu, Submenu
from app.database.database import get_db
from app.main import app
from app.redis.menu_redis import MenuRedis
from app.redis.redis_client import redis_client
from config import DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST, DB_USER_TEST

from .tests_data import dish_data, menu_data, submenu_data

DATABASE_URL = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

test_engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(bind=test_engine, class_=AsyncSession)
SQLModel.metadata.bind = test_engine


async def override_get_db() -> AsyncGenerator:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
async def prepare_database() -> AsyncGenerator:
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(autouse=True, scope='session')
async def prepare_redis():
    await redis_client.setup()


@pytest.fixture(scope='session')
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


async def db_cleanup(session: AsyncSession) -> None:
    """
    Clean up the database by deleting all data in the tables.
    This function does not delete the tables themselves.
    """
    # Delete all dishes
    await session.execute(delete(Dish))
    await session.commit()

    # Delete all submenus
    await session.execute(delete(Submenu))
    await session.commit()

    # Delete all menus
    await session.execute(delete(Menu))
    await session.commit()


@pytest.fixture()
async def create_menu(session: AsyncSession) -> AsyncGenerator[SQLModel, None]:
    new_menu = Menu(**menu_data)
    session.add(new_menu)
    await MenuRedis.clear_menus_data()
    await session.commit()
    await session.refresh(new_menu)
    yield new_menu


@pytest.fixture()
async def create_submenu(create_menu: Menu, session: AsyncSession) -> AsyncGenerator[SQLModel, None]:
    new_submenu = Submenu(**submenu_data, menu_id=create_menu.id)
    session.add(new_submenu)
    await MenuRedis.clear_menus_data()
    await session.commit()
    await session.refresh(new_submenu)
    yield new_submenu


@pytest.fixture()
async def create_dish(create_submenu: Submenu, session: AsyncSession) -> AsyncGenerator[SQLModel, None]:
    new_dish = Dish(**dish_data, submenu_id=create_submenu.id)
    session.add(new_dish)
    await MenuRedis.clear_menus_data()
    await session.commit()
    await session.refresh(new_dish)
    yield new_dish
