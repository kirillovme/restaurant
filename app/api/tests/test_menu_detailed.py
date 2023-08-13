import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.models.models import Dish, Menu, Submenu
from app.api.tests.conftest import db_cleanup
from app.util.reverse import reverse


@pytest.mark.run(order=13)
async def test_empty_base(client: AsyncClient, session: AsyncSession) -> None:
    await db_cleanup(session)
    response = await client.get(reverse('get_menus_details'))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == []


@pytest.mark.run(order=14)
async def test_menu_empty(client: AsyncClient, create_menu: Menu) -> None:
    response = await client.get(reverse('get_menus_details'))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    menu = None
    for menu_data in data:
        if menu_data['id'] == str(create_menu.id):
            menu = menu_data
    assert menu['id'] == str(create_menu.id)
    assert menu['title'] == create_menu.title
    assert menu['description'] == create_menu.description
    assert menu['submenus'] == []


@pytest.mark.run(order=15)
async def test_menu_submenu(client: AsyncClient, create_menu: Menu, create_submenu: Submenu) -> None:
    response = await client.get(reverse('get_menus_details'))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    menu = None
    for menu_data in data:
        if menu_data['id'] == str(create_menu.id):
            menu = menu_data
    submenu = menu['submenus'][0]
    assert submenu['id'] == str(create_submenu.id)
    assert submenu['title'] == create_submenu.title
    assert submenu['description'] == create_submenu.description
    assert submenu['dishes'] == []


@pytest.mark.run(order=16)
async def test_menu_submenu_dish(client: AsyncClient, create_menu: Menu, create_submenu: Submenu,
                                 create_dish: Dish) -> None:
    response = await client.get(reverse('get_menus_details'))
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    menu = None
    for menu_data in data:
        if menu_data['id'] == str(create_menu.id):
            menu = menu_data
    submenu = menu['submenus'][0]
    dish = submenu['dishes'][0]
    assert dish['id'] == str(create_dish.id)
    assert dish['title'] == create_dish.title
    assert dish['description'] == create_dish.description
    assert dish['price'] == f'{float(create_dish.price):.2f}'
