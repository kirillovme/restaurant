from fastapi import status
from httpx import AsyncClient

from app.api.models.models import Dish, Menu, Submenu
from app.util.reverse import reverse


async def test_create_dish(client: AsyncClient, create_menu: Menu, create_submenu: Submenu) -> None:
    dish_data = {'title': 'Тестовое блюдо', 'description': 'Тестовое описание блюда', 'price': 12.50}
    response = await client.post(reverse('create_dish', menu_id=create_menu.id, submenu_id=create_submenu.id),
                                 json=dish_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == dish_data['title']
    assert data['description'] == dish_data['description']
    assert data['price'] == f"{dish_data['price']:.2f}"
    assert 'id' in data


async def test_read_dish(client: AsyncClient, create_menu: Menu, create_submenu: Submenu, create_dish: Dish) -> None:
    response = await client.get(reverse('get_dish', menu_id=create_menu.id, submenu_id=create_submenu.id,
                                        dish_id=create_dish.id))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_dish.title
    assert data['description'] == create_dish.description
    assert data['price'] == f'{float(create_dish.price):.2f}'
    assert data['id'] == str(create_dish.id)


async def test_update_dish(client: AsyncClient, create_menu: Menu, create_submenu: Submenu, create_dish: Dish) -> None:
    update_dish_data = {'title': 'Тестовое обновление', 'description': 'Тестовое обновление блюда', 'price': 2000.50}
    response = await client.patch(
        reverse('update_dish', menu_id=create_menu.id, submenu_id=create_submenu.id, dish_id=create_dish.id),
        json=update_dish_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == update_dish_data['title']
    assert data['description'] == update_dish_data['description']
    assert data['price'] == f"{update_dish_data['price']:.2f}"
    assert data['id'] == str(create_dish.id)


async def test_delete_dish(client: AsyncClient, create_menu: Menu, create_submenu: Submenu, create_dish: Dish) -> None:
    response = await client.delete(
        reverse('delete_dish', menu_id=create_menu.id, submenu_id=create_submenu.id, dish_id=create_dish.id))
    assert response.status_code == status.HTTP_200_OK
    response = await client.get(
        reverse('get_dish', menu_id=create_menu.id, submenu_id=create_submenu.id, dish_id=create_dish.id))
    assert response.status_code == status.HTTP_404_NOT_FOUND
