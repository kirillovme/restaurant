from fastapi.testclient import TestClient
from app.main import app
from fastapi import status
import pytest


def test_create_menu(client):
    menu_data = {'title': 'Тестовое меню', 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['title'] == menu_data['title']
    assert data['description'] == menu_data['description']
    assert "id" in data


def test_read_menu(client, create_menu):
    response = client.get(f"/api/v1/menus/{create_menu['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == create_menu['title']
    assert data['description'] == create_menu['description']
    assert data['id'] == create_menu['id']


def test_update_menu(client, create_menu):
    updated_menu_data = {'title': 'Тестовое обновление', 'description': 'Тестовое обновление описания'}
    response = client.patch(f"/api/v1/menus/{create_menu['id']}", json=updated_menu_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['title'] == updated_menu_data['title']
    assert data['description'] == updated_menu_data['description']
    assert data['id'] == create_menu['id']


def test_delete_menu(client, create_menu):
    response = client.delete(f"/api/v1/menus/{create_menu['id']}")
    assert response.status_code == status.HTTP_200_OK
    response = client.get(f"/api/v1/menus/{create_menu['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
