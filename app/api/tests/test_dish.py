from fastapi import status


def test_create_dish(client, create_menu, create_submenu):
    dish_data = {'title': 'Тестовое блюдо', 'description': 'Тестовое описание блюда', 'price': 12.50}
    response = client.post(f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes", json=dish_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']
    assert data['price'] == f"{dish_data['price']:.2f}"
    assert "id" in data


def test_read_dish(client, create_menu, create_submenu, create_dish):
    response = client.get(
        f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{create_dish['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_dish['title']
    assert data['description'] == create_dish['description']
    assert data['price'] == f"{float(create_dish['price']):.2f}"
    assert data['id'] == create_dish['id']


def test_update_dish(client, create_menu, create_submenu, create_dish):
    update_dish_data = {'title': 'Тестовое обновление', 'description': 'Тестовое обновление блюда', 'price': 2000.50}
    response = client.patch(
        f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{create_dish['id']}",
        json=update_dish_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == update_dish_data['title']
    assert data['description'] == update_dish_data['description']
    assert data['price'] == f"{update_dish_data['price']:.2f}"
    assert data['id'] == create_dish['id']


def test_delete_dish(client, create_menu, create_submenu, create_dish):
    response = client.delete(
        f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{create_dish['id']}")
    assert response.status_code == status.HTTP_200_OK
    response = client.get(
        f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}/dishes/{create_dish['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
