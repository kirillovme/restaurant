from fastapi import status
from fastapi.testclient import TestClient

from app.util.reverse import reverse


def test_create_dish(client: TestClient, create_menu: dict, create_submenu: dict) -> None:
    dish_data = {'title': 'Тестовое блюдо', 'description': 'Тестовое описание блюда', 'price': 12.50}
    response = client.post(reverse('create_dish', menu_id=create_menu['id'], submenu_id=create_submenu['id']),
                           json=dish_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']
    assert data['price'] == f"{dish_data['price']:.2f}"
    assert 'id' in data


def test_read_dish(client: TestClient, create_menu: dict, create_submenu: dict, create_dish: dict) -> None:
    response = client.get(reverse('get_dish', menu_id=create_menu['id'], submenu_id=create_submenu['id'],
                                  dish_id=create_dish['id']))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_dish['title']
    assert data['description'] == create_dish['description']
    assert data['price'] == f"{float(create_dish['price']):.2f}"
    assert data['id'] == create_dish['id']


def test_update_dish(client: TestClient, create_menu: dict, create_submenu: dict, create_dish: dict) -> None:
    update_dish_data = {'title': 'Тестовое обновление', 'description': 'Тестовое обновление блюда', 'price': 2000.50}
    response = client.patch(
        reverse('update_dish', menu_id=create_menu['id'], submenu_id=create_submenu['id'], dish_id=create_dish['id']),
        json=update_dish_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == update_dish_data['title']
    assert data['description'] == update_dish_data['description']
    assert data['price'] == f"{update_dish_data['price']:.2f}"
    assert data['id'] == create_dish['id']


def test_delete_dish(client: TestClient, create_menu: dict, create_submenu: dict, create_dish: dict) -> None:
    response = client.delete(
        reverse('delete_dish', menu_id=create_menu['id'], submenu_id=create_submenu['id'], dish_id=create_dish['id']))
    assert response.status_code == status.HTTP_200_OK
    response = client.get(
        reverse('get_dish', menu_id=create_menu['id'], submenu_id=create_submenu['id'], dish_id=create_dish['id']))
    assert response.status_code == status.HTTP_404_NOT_FOUND
