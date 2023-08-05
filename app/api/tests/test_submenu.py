from fastapi import status


def test_create_submenu(client, create_menu):
    submenu_data = {'title': 'Тестовое подменю', 'description': 'Тестовое подменю'}
    response = client.post(f"/api/v1/menus/{create_menu['id']}/submenus", json=submenu_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == submenu_data['title']
    assert "id" in data
    assert data['description'] == submenu_data['description']


def test_read_submenu(client, create_menu, create_submenu):
    response = client.get(f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_submenu['title']
    assert data['description'] == create_submenu['description']
    assert data['id'] == create_submenu['id']


def test_update_submenu(client, create_menu, create_submenu):
    updated_submenu_data = {'title': 'Обновленное значение', 'description': 'Обновленное описание'}
    response = client.patch(f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}",
                            json=updated_submenu_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == updated_submenu_data['title']
    assert data['description'] == updated_submenu_data['description']
    assert data['id'] == create_submenu['id']


def test_delete_submenu(client, create_menu, create_submenu):
    response = client.delete(f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}")
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f"/api/v1/menus/{create_menu['id']}/submenus/{create_submenu['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
