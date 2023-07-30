from fastapi.testclient import TestClient
from app.main import app
from fastapi import status

client = TestClient(app)


def test_create_dish():
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

    dish_data = {'title': 'Тестовое блюдо',
                 'description': 'Тестовое описание блюда',
                 'price': 12.50}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']
    assert data['price'] == f"{dish_data['price']:.2f}"
    assert "id" in data


def test_read_dish():
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

    dish_data = {'title': 'Тестовое блюдо',
                 'description': 'Тестовое описание блюда',
                 'price': 12.50}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)

    assert response.status_code == status.HTTP_201_CREATED

    created_dish = response.json()

    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes/" +
                          f"{created_dish['id']}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']
    assert data['price'] == f"{dish_data['price']:.2f}"
    assert data['id'] == created_dish['id']


def test_update_dish():
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

    dish_data = {'title': 'Тестовое блюдо',
                 'description': 'Тестовое описание блюда',
                 'price': 12.50}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)

    assert response.status_code == status.HTTP_201_CREATED

    created_dish = response.json()

    update_dish_data = {'title': 'Тестовое обновление',
                        'description': 'Тестовое обновление блюда',
                        'price': 2000.50}

    response = client.patch(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes/" +
                            f"{created_dish['id']}", json=update_dish_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['title'] == update_dish_data['title']
    assert data['description'] == update_dish_data['description']
    assert data['price'] == f"{update_dish_data['price']:.2f}"
    assert data['id'] == created_dish['id']


def test_delete_dish():
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

    dish_data = {'title': 'Тестовое блюдо',
                 'description': 'Тестовое описание блюда',
                 'price': 12.50}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)

    assert response.status_code == status.HTTP_201_CREATED

    created_dish = response.json()

    response = client.delete(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes/" +
                             f"{created_dish['id']}")

    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes/" +
                             f"{created_dish['id']}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
