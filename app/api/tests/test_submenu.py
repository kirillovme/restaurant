from fastapi import status
from fastapi.testclient import TestClient

from app.util.reverse import reverse


def test_create_submenu(client: TestClient, create_menu: dict) -> None:
    submenu_data = {'title': 'Тестовое подменю', 'description': 'Тестовое подменю'}
    response = client.post(reverse('create_submenu', menu_id=create_menu['id']), json=submenu_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == submenu_data['title']
    assert 'id' in data
    assert data['description'] == submenu_data['description']


def test_read_submenu(client: TestClient, create_menu: dict, create_submenu: dict) -> None:
    response = client.get(reverse('get_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_submenu['title']
    assert data['description'] == create_submenu['description']
    assert data['id'] == create_submenu['id']


def test_update_submenu(client: TestClient, create_menu: dict, create_submenu: dict) -> None:
    updated_submenu_data = {'title': 'Обновленное значение', 'description': 'Обновленное описание'}
    response = client.patch(reverse('update_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']),
                            json=updated_submenu_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == updated_submenu_data['title']
    assert data['description'] == updated_submenu_data['description']
    assert data['id'] == create_submenu['id']


def test_delete_submenu(client: TestClient, create_menu: dict, create_submenu: dict) -> None:
    response = client.delete(reverse('delete_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']))
    assert response.status_code == status.HTTP_200_OK
    response = client.get(reverse('get_submenu', menu_id=create_menu['id'], submenu_id=create_submenu['id']))
    assert response.status_code == status.HTTP_404_NOT_FOUND
