from fastapi.testclient import TestClient
from app.main import app
from fastapi import status
from .conftest import db_cleanup

client = TestClient(app)


def test_dishes_scenario():
    # Cleaning db
    db_cleanup()
    # Creating menu
    menu_data = {'title': 'Тестовое меню',
                 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)

    created_menu = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_menu

    # Creating submenu
    submenu_data = {'title': 'Тестовое подменю',
                    'description': 'Тестовое подменю'}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus", json=submenu_data)

    created_submenu = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_menu

    # Creating first dish
    dish_data = {'title': 'Тестовое блюдо',
                 'description': 'Тестовое описание блюда',
                 'price': 12.50}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)

    created_dish1 = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_menu

    # Creating second dish
    dish_data = {'title': 'Тестовое блюдо 2',
                 'description': 'Тестовое описание блюда 2',
                 'price': 12.51}

    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)

    created_dish2 = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_menu

    # Checkin counts in menu after creating submenu and 2 dishes
    response = client.get(f"/api/v1/menus/{created_menu['id']}")

    menu_get_after_creation = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert menu_get_after_creation['submenus_count'] == 1
    assert menu_get_after_creation['dishes_count'] == 2
    assert created_menu["id"] == menu_get_after_creation['id']

    # Checking counts in submenu after creating 2 dishes
    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}")

    submenu_get_after_creation = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert submenu_get_after_creation['dishes_count'] == 2
    assert submenu_get_after_creation['id'] == created_submenu['id']

    # Deleting submenu
    response = client.delete(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}")

    assert response.status_code == status.HTTP_200_OK

    # Checking submenus of menu after deletion
    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus")

    submenus_list_view = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert submenus_list_view == []

    # Checking dishes of deleted submenu
    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes")

    dishes_after_deletion_submenu = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert dishes_after_deletion_submenu == []

    # Checking counts of menu after deletion of submenu
    response = client.get(f"/api/v1/menus/{created_menu['id']}")

    menu_after_deletion_submenu = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert menu_after_deletion_submenu['id'] == created_menu['id']
    assert menu_after_deletion_submenu['submenus_count'] == 0
    assert menu_after_deletion_submenu['dishes_count'] == 0

    # Deleting menu
    response = client.delete(f"/api/v1/menus/{created_menu['id']}")

    assert response.status_code == status.HTTP_200_OK

    # Checking menu list after menu deletion
    response = client.get(f"/api/v1/menus")

    data_after_deletion_menu = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data_after_deletion_menu == []
