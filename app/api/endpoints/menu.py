from fastapi import APIRouter, Depends
from app.api.schemas import schemas
from app.api.services.menu_service import MenuService


router = APIRouter()


@router.get('/menus')
def get_menus(menu_service: MenuService = Depends()):
    return menu_service.get_items()


@router.post('/menus')
def create_menu(menu_data: schemas.Menu, menu_service: MenuService = Depends()):
    return menu_service.create(menu_data)


@router.get('/menus/{menu_id}')
def get_menu(menu_id: int, menu_service: MenuService = Depends()):
    return menu_service.get_item(menu_id)


@router.patch('/menus/{menu_id}')
def update_menu(menu_id: int, menu_data: schemas.Menu, menu_service: MenuService = Depends()):
    return menu_service.update_item(menu_id, menu_data)


@router.delete('/menus/{menu_id}')
def delete_menu(menu_id: int, menu_service: MenuService = Depends()):
    return menu_service.delete_item(menu_id)
