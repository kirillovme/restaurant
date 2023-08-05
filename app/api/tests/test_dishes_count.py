import pytest
from fastapi import status
from .conftest import db_cleanup


@pytest.mark.run(order=1)
def test_create_menu(client):
    db_cleanup()
    global created_menu
    menu_data = {'title': 'Тестовое меню', 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)
    created_menu = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_menu


@pytest.mark.run(order=2)
def test_create_submenu(client):
    global created_submenu
    submenu_data = {'title': 'Тестовое подменю', 'description': 'Тестовое подменю'}
    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus", json=submenu_data)
    created_submenu = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_submenu


@pytest.mark.run(order=3)
def test_create_first_dish(client):
    global created_dish1
    dish_data = {'title': 'Тестовое блюдо', 'description': 'Тестовое описание блюда', 'price': 12.50}
    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)
    created_dish1 = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_dish1


@pytest.mark.run(order=4)
def test_create_second_dish(client):
    global created_dish2
    dish_data = {'title': 'Тестовое блюдо 2', 'description': 'Тестовое описание блюда 2', 'price': 12.51}
    response = client.post(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes",
                           json=dish_data)
    created_dish2 = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in created_dish2


@pytest.mark.run(order=5)
def test_check_counts_in_menu_after_creation(client):
    response = client.get(f"/api/v1/menus/{created_menu['id']}")
    menu_get_after_creation = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert menu_get_after_creation['submenus_count'] == 1
    assert menu_get_after_creation['dishes_count'] == 2
    assert created_menu["id"] == menu_get_after_creation['id']


@pytest.mark.run(order=6)
def test_check_counts_in_submenu_after_creation(client):
    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}")
    submenu_get_after_creation = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert submenu_get_after_creation['dishes_count'] == 2
    assert submenu_get_after_creation['id'] == created_submenu['id']


@pytest.mark.run(order=7)
def test_delete_submenu(client):
    response = client.delete(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.run(order=8)
def test_check_submenus_after_deletion(client):
    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus")
    submenus_list_view = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert submenus_list_view == []


@pytest.mark.run(order=9)
def test_check_dishes_of_deleted_submenu(client):
    response = client.get(f"/api/v1/menus/{created_menu['id']}/submenus/{created_submenu['id']}/dishes")
    dishes_after_deletion_submenu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert dishes_after_deletion_submenu == []


@pytest.mark.run(order=10)
def test_check_counts_of_menu_after_deletion_of_submenu(client):
    response = client.get(f"/api/v1/menus/{created_menu['id']}")
    menu_after_deletion_submenu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert menu_after_deletion_submenu['id'] == created_menu['id']
    assert menu_after_deletion_submenu['submenus_count'] == 0
    assert menu_after_deletion_submenu['dishes_count'] == 0


@pytest.mark.run(order=11)
def test_delete_menu(client):
    response = client.delete(f"/api/v1/menus/{created_menu['id']}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.run(order=12)
def test_check_menu_list_after_menu_deletion(client):
    response = client.get("/api/v1/menus")
    data_after_deletion_menu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data_after_deletion_menu == []
