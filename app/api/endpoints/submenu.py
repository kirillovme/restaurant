from fastapi import APIRouter, Depends
from app.api.schemas import schemas
from app.api.services.submenu_service import SubmenuService

router = APIRouter()


@router.get('/submenus')
def get_submenus(menu_id: int, submenu_service: SubmenuService = Depends()):
    return submenu_service.get_items(menu_id)


@router.post('/submenus')
def create_submenu(menu_id: int, submenu_data: schemas.Submenu, submenu_service: SubmenuService = Depends()):
    return submenu_service.create_item(menu_id, submenu_data)


@router.get('/submenus/{submenu_id}')
def get_submenu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends()):
    return submenu_service.get_item(menu_id, submenu_id)


@router.patch('/submenus/{submenu_id}')
def update_menu(menu_id: int, submenu_id: int, submenu_data: schemas.Submenu,
                submenu_service: SubmenuService = Depends()):
    return submenu_service.update_item(menu_id, submenu_id, submenu_data)


@router.delete('/submenus/{submenu_id}')
def delete_menu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends()):
    return submenu_service.delete_item(menu_id, submenu_id)
