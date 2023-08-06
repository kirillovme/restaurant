from fastapi import status
from fastapi.testclient import TestClient

from app.util.reverse import reverse


def test_create_menu(client: TestClient) -> None:
    menu_data = {'title': 'Тестовое меню', 'description': 'Тестовое описание'}
    response = client.post(reverse('create_menu'), json=menu_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']
    assert 'id' in data


def test_read_menu(client: TestClient, create_menu: dict) -> None:
    response = client.get(reverse('get_menu', menu_id=create_menu['id']))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_menu['title']
    assert data['description'] == create_menu['description']
    assert data['id'] == create_menu['id']


def test_update_menu(client: TestClient, create_menu: dict) -> None:
    updated_menu_data = {'title': 'Тестовое обновление', 'description': 'Тестовое обновление описания'}
    response = client.patch(reverse('update_menu', menu_id=create_menu['id']), json=updated_menu_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == updated_menu_data['title']
    assert data['description'] == updated_menu_data['description']
    assert data['id'] == create_menu['id']


def test_delete_menu(client: TestClient, create_menu: dict) -> None:
    response = client.delete(reverse('delete_menu', menu_id=create_menu['id']))
    assert response.status_code == status.HTTP_200_OK
    response = client.get(reverse('get_menu', menu_id=create_menu['id']))
    assert response.status_code == status.HTTP_404_NOT_FOUND
