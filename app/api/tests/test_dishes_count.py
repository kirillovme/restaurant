import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.tests.conftest import db_cleanup
from app.util.reverse import reverse


@pytest.mark.run(order=1)
async def test_create_menu(client: AsyncClient, session: AsyncSession) -> None:
    await db_cleanup(session)
    global created_menu
    menu_data = {'title': 'Тестовое меню', 'description': 'Тестовое описание'}
    response = await client.post(reverse('create_menu'), json=menu_data)
    created_menu = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in created_menu


@pytest.mark.run(order=2)
async def test_create_submenu(client: AsyncClient) -> None:
    global created_submenu
    submenu_data = {'title': 'Тестовое подменю', 'description': 'Тестовое подменю'}
    response = await client.post(reverse('create_submenu', menu_id=created_menu['id']), json=submenu_data)
    created_submenu = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in created_submenu


@pytest.mark.run(order=3)
async def test_create_first_dish(client: AsyncClient) -> None:
    global created_dish1
    dish_data = {'title': 'Тестовое блюдо', 'description': 'Тестовое описание блюда', 'price': 12.50}
    response = await client.post(reverse('create_dish', menu_id=created_menu['id'], submenu_id=created_submenu['id']),
                                 json=dish_data)
    created_dish1 = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in created_dish1


@pytest.mark.run(order=4)
async def test_create_second_dish(client: AsyncClient) -> None:
    global created_dish2
    dish_data = {'title': 'Тестовое блюдо 2', 'description': 'Тестовое описание блюда 2', 'price': 12.51}
    response = await client.post(reverse('create_dish', menu_id=created_menu['id'], submenu_id=created_submenu['id']),
                                 json=dish_data)
    created_dish2 = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in created_dish2


@pytest.mark.run(order=5)
async def test_check_counts_in_menu_after_creation(client: AsyncClient) -> None:
    response = await client.get(reverse('get_menu', menu_id=created_menu['id']))
    menu_get_after_creation = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert menu_get_after_creation['submenus_count'] == 1
    assert menu_get_after_creation['dishes_count'] == 2
    assert created_menu['id'] == menu_get_after_creation['id']


@pytest.mark.run(order=6)
async def test_check_counts_in_submenu_after_creation(client: AsyncClient) -> None:
    response = await client.get(reverse('get_submenu', menu_id=created_menu['id'], submenu_id=created_submenu['id']))
    submenu_get_after_creation = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert submenu_get_after_creation['dishes_count'] == 2
    assert submenu_get_after_creation['id'] == created_submenu['id']


@pytest.mark.run(order=7)
async def test_delete_submenu(client: AsyncClient) -> None:
    response = await client.delete(reverse('delete_submenu', menu_id=created_menu['id'], submenu_id=created_submenu['id']))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.run(order=8)
async def test_check_submenus_after_deletion(client: AsyncClient) -> None:
    response = await client.get(reverse('get_submenus', menu_id=created_menu['id']))
    submenus_list_view = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert submenus_list_view == []


@pytest.mark.run(order=9)
async def test_check_dishes_of_deleted_submenu(client: AsyncClient) -> None:
    response = await client.get(reverse('get_dishes', menu_id=created_menu['id'], submenu_id=created_submenu['id']))
    dishes_after_deletion_submenu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert dishes_after_deletion_submenu == []


@pytest.mark.run(order=10)
async def test_check_counts_of_menu_after_deletion_of_submenu(client: AsyncClient) -> None:
    response = await client.get(reverse('get_menu', menu_id=created_menu['id']))
    menu_after_deletion_submenu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert menu_after_deletion_submenu['id'] == created_menu['id']
    assert menu_after_deletion_submenu['submenus_count'] == 0
    assert menu_after_deletion_submenu['dishes_count'] == 0


@pytest.mark.run(order=11)
async def test_delete_menu(client: AsyncClient) -> None:
    response = await client.delete(reverse('delete_menu', menu_id=created_menu['id']))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.run(order=12)
async def test_check_menu_list_after_menu_deletion(client: AsyncClient) -> None:
    response = await client.get(reverse('get_menus'))
    data_after_deletion_menu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data_after_deletion_menu == []
