from fastapi import APIRouter, BackgroundTasks, Depends
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
async def get_menus(menu_service: MenuService = Depends()) -> list[dict]:
    return await menu_service.get_items()


@router.get('/menus/details',
            summary='Fetches a list of all menus in detail',
            description='Return a list of all avaliable menus with submenus with dishes',
            tags=['Menus'],
            response_model=list[schemas.MenuDetailedResponse],
            name='get_menus_details')
async def get_menus_details(menu_service: MenuService = Depends()) -> list[dict]:
    return await menu_service.get_items_details()


@router.post('/menus',
             summary='Creates a new menu',
             description='Creates a new menu with the provided data.',
             tags=['Menus'],
             response_model=schemas.MenuResponse,
             name='create_menu')
async def create_menu(menu_data: schemas.Menu, background_tasks: BackgroundTasks,
                      menu_service: MenuService = Depends()) -> JSONResponse:
    return await menu_service.create(menu_data, background_tasks)


@router.get('/menus/{menu_id}', summary='Retrieves a specific menu by its ID',
            description='Returns the menu with the specified ID.',
            tags=['Menus'],
            response_model=schemas.MenuResponse,
            name='get_menu')
async def get_menu(menu_id: int, menu_service: MenuService = Depends()) -> JSONResponse:
    return await menu_service.get_item(menu_id)


@router.patch('/menus/{menu_id}', summary='Updates a specific menu by its ID',
              description='Updates the menu with the specified ID.',
              tags=['Menus'],
              response_model=schemas.MenuResponse,
              name='update_menu')
async def update_menu(menu_id: int, menu_data: schemas.Menu, background_tasks: BackgroundTasks,
                      menu_service: MenuService = Depends()) -> JSONResponse:
    return await menu_service.update_item(menu_id, menu_data, background_tasks)


@router.delete('/menus/{menu_id}', summary='Deletes a specific menu by its ID',
               description='Deletes the menu with the specified ID.',
               tags=['Menus'],
               response_model=schemas.MenuResponse,
               name='delete_menu')
async def delete_menu(menu_id: int, background_tasks: BackgroundTasks,
                      menu_service: MenuService = Depends()) -> JSONResponse:
    return await menu_service.delete_item(menu_id, background_tasks)
