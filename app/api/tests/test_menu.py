from fastapi.testclient import TestClient
from app.main import app
from fastapi import status
import pytest

client = TestClient(app)


def test_create_menu():
    menu_data = {'title': 'Тестовое меню',
                 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']
    assert "id" in data


def test_read_menu():
    menu_data = {'title': 'Тестовое меню 223',
                 'description': 'Тестовое описание 223'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()

    response = client.get(f"/api/v1/menus/{created_menu['id']}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']
    assert data['id'] == created_menu['id']


def test_update_menu():
    menu_data = {'title': 'Тестовое меню 223',
                 'description': 'Тестовое описание 223'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()

    updated_menu_data = {'title': 'Тестовое обновление',
                         'description': 'Тестовое обновление описания'}
    response = client.patch(f"/api/v1/menus/{created_menu['id']}", json=updated_menu_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['title'] == updated_menu_data['title']
    assert data['description'] == updated_menu_data['description']
    assert data['id'] == created_menu['id']


def test_delete_menu():
    menu_data = {'title': 'Тестовое меню 223',
                 'description': 'Тестовое описание 223'}
    response = client.post("/api/v1/menus", json=menu_data)

    assert response.status_code == status.HTTP_201_CREATED
    created_menu = response.json()

    response = client.delete(f"/api/v1/menus/{created_menu['id']}")

    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/api/v1/menus/{created_menu['id']}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
