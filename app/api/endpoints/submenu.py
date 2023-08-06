from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.schemas import schemas
from app.api.services.submenu_service import SubmenuService

router = APIRouter()


@router.get('/submenus',
            summary='Fetches all submenus for a menu',
            description='Returns a list of all submenus for the specified menu ID.',
            tags=['Submenus'],
            response_model=list[schemas.SubmenuResponse],
            name='get_submenus')
def get_submenus(menu_id: int, submenu_service: SubmenuService = Depends()) -> list[dict]:
    return submenu_service.get_items(menu_id)


@router.post('/submenus',
             summary='Creates a new submenu for a menu',
             description='Creates a new submenu for the specified menu ID.',
             tags=['Submenus'],
             response_model=schemas.SubmenuResponse,
             name='create_submenu')
def create_submenu(menu_id: int,
                   submenu_data: schemas.Submenu,
                   submenu_service: SubmenuService = Depends()) -> JSONResponse:
    return submenu_service.create_item(menu_id, submenu_data)


@router.get('/submenus/{submenu_id}',
            summary='Retrieves a specific submenu',
            description='Returns the submenu with the specified submenu ID for the given menu ID.',
            tags=['Submenus'],
            response_model=schemas.SubmenuResponse,
            name='get_submenu')
def get_submenu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends()):
    return submenu_service.get_item(menu_id, submenu_id)


@router.patch('/submenus/{submenu_id}',
              summary='Updates a specific submenu',
              description='Updates the submenu with the specified submenu ID for the given menu ID.',
              tags=['Submenus'],
              response_model=schemas.SubmenuResponse,
              name='update_submenu')
def update_menu(menu_id: int, submenu_id: int, submenu_data: schemas.Submenu,
                submenu_service: SubmenuService = Depends()) -> JSONResponse:
    return submenu_service.update_item(menu_id, submenu_id, submenu_data)


@router.delete('/submenus/{submenu_id}',
               summary='Deletes a specific submenu',
               description='Deletes the submenu with the specified submenu ID for the given menu ID.',
               tags=['Submenus'],
               response_model=schemas.SubmenuResponse,
               name='delete_submenu')
def delete_menu(menu_id: int, submenu_id: int, submenu_service: SubmenuService = Depends()) -> JSONResponse:
    return submenu_service.delete_item(menu_id, submenu_id)
