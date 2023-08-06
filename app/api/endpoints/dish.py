from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.api.schemas import schemas
from app.api.services.dish_service import DishService

router = APIRouter()


@router.get('/dishes',
            summary='Fetches all dishes for a submenu',
            description='Returns a list of all dishes for the specified menu ID and submenu ID.',
            tags=['Dishes'],
            response_model=list[schemas.DishResponse],
            name='get_dishes')
def get_dishes(menu_id: int, submenu_id: int, dish_service: DishService = Depends()) -> JSONResponse:
    return dish_service.get_items(menu_id, submenu_id)


@router.post('/dishes',
             summary='Creates a new dish for a submenu',
             description='Creates a new dish for the specified menu ID and submenu ID.',
             tags=['Dishes'],
             response_model=schemas.DishResponse,
             name='create_dish')
def create_dish(menu_id: int,
                submenu_id: int,
                dish_data: schemas.Dish,
                dish_service: DishService = Depends()) -> JSONResponse:
    return dish_service.create_item(menu_id, submenu_id, dish_data)


@router.get('/dishes/{dish_id}',
            summary='Retrieves a specific dish',
            description='Returns the dish with the specified dish ID for the given menu ID and submenu ID.',
            tags=['Dishes'],
            response_model=schemas.DishResponse,
            name='get_dish')
def get_dish(menu_id: int, submenu_id: int, dish_id: int, dish_service: DishService = Depends()) -> JSONResponse:
    return dish_service.get_item(menu_id, submenu_id, dish_id)


@router.patch('/dishes/{dish_id}',
              summary='Updates a specific dish',
              description='Updates the dish with the specified dish ID for the given menu ID and submenu ID.',
              tags=['Dishes'],
              response_model=schemas.DishResponse,
              name='update_dish')
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish_data: schemas.Dish,
                dish_service: DishService = Depends()) -> JSONResponse:
    return dish_service.update_item(menu_id, submenu_id, dish_id, dish_data)


@router.delete('/dishes/{dish_id}',
               summary='Deletes a specific dish',
               description='Deletes the dish with the specified dish ID for the given menu ID and submenu ID.',
               tags=['Dishes'],
               response_model=schemas.DishResponse,
               name='delete_dish')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, dish_service: DishService = Depends()) -> JSONResponse:
    return dish_service.delete_item(menu_id, submenu_id, dish_id)
