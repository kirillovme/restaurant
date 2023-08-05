from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.api.models import models
from app.api.schemas import schemas
from app.database.database import get_db
from fastapi.responses import JSONResponse
from app.api.services.dish_service import DishService

router = APIRouter()


@router.get('/dishes')
def get_dishes(menu_id: int, submenu_id: int, dish_service: DishService = Depends()):
    return dish_service.get_items(menu_id, submenu_id)


@router.post('/dishes')
def create_dish(menu_id: int, submenu_id: int, dish_data: schemas.Dish, dish_service: DishService = Depends()):
    return dish_service.create_item(menu_id, submenu_id, dish_data)


@router.get('/dishes/{dish_id}')
def get_dish(menu_id: int, submenu_id: int, dish_id: int, dish_service: DishService = Depends()):
    return dish_service.get_item(menu_id, submenu_id, dish_id)


@router.patch('/dishes/{dish_id}')
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish_data: schemas.Dish,
                dish_service: DishService = Depends()):
    return dish_service.update_item(menu_id, submenu_id, dish_id, dish_data)


@router.delete('/dishes/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, dish_service: DishService = Depends()):
    return dish_service.delete_item(menu_id, submenu_id, dish_id)
