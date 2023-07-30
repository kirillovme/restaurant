from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app)


def test_create_submenu():
    menu_data = {'title': 'Тестовое меню',
                 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()

    submenu_data = {'title': 'Тестовое подменю',
                    'description': 'Тестовое подменю'}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus", json=submenu_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data['title'] == submenu_data['title']
    assert "id" in data
    assert data['description'] == submenu_data['description']


def test_read_submenu():
    menu_data = {'title': 'Тестовое меню',
                 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()

    submenu_data = {'title': 'Тестовое подменю',
                    'description': 'Тестовое подменю'}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus", json=submenu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_submenu = response.json()

    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['title'] == submenu_data['title']
    assert data['description'] == submenu_data['description']
    assert data['id'] == created_submenu['id']


def test_update_submenu():
    menu_data = {'title': 'Тестовое меню',
                 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()

    submenu_data = {'title': 'Тестовое подменю',
                    'description': 'Тестовое подменю'}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus", json=submenu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_submenu = response.json()

    updated_submenu_data = {'title': 'Обновленное значение',
                            'description': 'Обновленное описание'}

    response = client.patch(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}",
                            json=updated_submenu_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['title'] == updated_submenu_data['title']
    assert data['description'] == updated_submenu_data['description']
    assert data['id'] == created_submenu['id']


def test_delete_submenu():
    menu_data = {'title': 'Тестовое меню',
                 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()

    submenu_data = {'title': 'Тестовое подменю',
                    'description': 'Тестовое подменю'}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus", json=submenu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_submenu = response.json()

    response = client.delete(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}")

    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


