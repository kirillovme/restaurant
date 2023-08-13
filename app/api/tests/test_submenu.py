from fastapi import status
from httpx import AsyncClient

from app.api.models.models import Menu, Submenu
from app.util.reverse import reverse


async def test_create_submenu(client: AsyncClient, create_menu: Menu) -> None:
    submenu_data = {'title': 'Тестовое подменю', 'description': 'Тестовое подменю'}
    response = await client.post(reverse('create_submenu', menu_id=create_menu.id), json=submenu_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == submenu_data['title']
    assert 'id' in data
    assert data['description'] == submenu_data['description']


async def test_read_submenu(client: AsyncClient, create_menu: Menu, create_submenu: Submenu) -> None:
    response = await client.get(reverse('get_submenu', menu_id=create_menu.id, submenu_id=create_submenu.id))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_submenu.title
    assert data['description'] == create_submenu.description
    assert data['id'] == str(create_submenu.id)


async def test_update_submenu(client: AsyncClient, create_menu: Menu, create_submenu: Submenu) -> None:
    updated_submenu_data = {'title': 'Обновленное значение', 'description': 'Обновленное описание'}
    response = await client.patch(reverse('update_submenu', menu_id=create_menu.id, submenu_id=create_submenu.id),
                                  json=updated_submenu_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == updated_submenu_data['title']
    assert data['description'] == updated_submenu_data['description']
    assert data['id'] == str(create_submenu.id)


async def test_delete_submenu(client: AsyncClient, create_menu: Menu, create_submenu: Submenu) -> None:
    response = await client.delete(reverse('delete_submenu', menu_id=create_menu.id, submenu_id=create_submenu.id))
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(reverse('get_submenu', menu_id=create_menu.id, submenu_id=create_submenu.id))
    assert response.status_code == status.HTTP_404_NOT_FOUND
