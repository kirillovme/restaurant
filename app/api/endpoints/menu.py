from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.schemas import schemas
from app.api.services.menu_service import MenuService

router = APIRouter()


@router.get('/menus',
            summary='Fetches a list of all menus',
            description='Returns a list of all available menus.',
            tags=['Menus'],
            response_model=list[schemas.MenuResponse],
            name='get_menus')
def get_menus(menu_service: MenuService = Depends()) -> list[dict]:
    return menu_service.get_items()


@router.post('/menus',
             summary='Creates a new menu',
             description='Creates a new menu with the provided data.',
             tags=['Menus'],
             response_model=schemas.MenuResponse,
             name='create_menu')
def create_menu(menu_data: schemas.Menu, menu_service: MenuService = Depends()) -> JSONResponse:
    return menu_service.create(menu_data)


@router.get('/menus/{menu_id}', summary='Retrieves a specific menu by its ID',
            description='Returns the menu with the specified ID.',
            tags=['Menus'],
            response_model=schemas.MenuResponse,
            name='get_menu')
def get_menu(menu_id: int, menu_service: MenuService = Depends()) -> JSONResponse:
    return menu_service.get_item(menu_id)


@router.patch('/menus/{menu_id}', summary='Updates a specific menu by its ID',
              description='Updates the menu with the specified ID.',
              tags=['Menus'],
              response_model=schemas.MenuResponse,
              name='update_menu')
def update_menu(menu_id: int, menu_data: schemas.Menu, menu_service: MenuService = Depends()) -> JSONResponse:
    return menu_service.update_item(menu_id, menu_data)


@router.delete('/menus/{menu_id}', summary='Deletes a specific menu by its ID',
               description='Deletes the menu with the specified ID.',
               tags=['Menus'],
               response_model=schemas.MenuResponse,
               name='delete_menu')
def delete_menu(menu_id: int, menu_service: MenuService = Depends()) -> JSONResponse:
    return menu_service.delete_item(menu_id)
