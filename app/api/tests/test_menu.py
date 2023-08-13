from fastapi import status
from httpx import AsyncClient

from app.api.models.models import Menu
from app.util.reverse import reverse


async def test_create_menu(client: AsyncClient) -> None:
    menu_data = {'title': 'Тестовое меню', 'description': 'Тестовое описание'}
    response = await client.post(reverse('create_menu'), json=menu_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']
    assert 'id' in data


async def test_read_menu(client: AsyncClient, create_menu: Menu) -> None:
    response = await client.get(reverse('get_menu', menu_id=create_menu.id))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_menu.title
    assert data['description'] == create_menu.description
    assert data['id'] == str(create_menu.id)


async def test_update_menu(client: AsyncClient, create_menu: Menu) -> None:
    updated_menu_data = {'title': 'Тестовое обновление', 'description': 'Тестовое обновление описания'}
    response = await client.patch(reverse('update_menu', menu_id=create_menu.id), json=updated_menu_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == updated_menu_data['title']
    assert data['description'] == updated_menu_data['description']
    assert data['id'] == str(create_menu.id)


async def test_delete_menu(client: AsyncClient, create_menu: Menu) -> None:
    response = await client.delete(reverse('delete_menu', menu_id=create_menu.id))
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(reverse('get_menu', menu_id=create_menu.id))
    assert response.status_code == status.HTTP_404_NOT_FOUND
