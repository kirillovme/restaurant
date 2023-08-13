import pickle

from fastapi import BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from app.api.repositories.dish_repository import DishRepository
from app.api.schemas import schemas
from app.redis.dish_redis import DishRedis
from app.redis.submenu_redis import SubmenuRedis


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends()) -> None:
        self.dish_repository = dish_repository

    async def get_items(self, menu_id: int, submenu_id: int) -> list[dict]:
        dish_redis = await DishRedis.get_dishes(menu_id, submenu_id)
        if dish_redis:
            return pickle.loads(dish_redis)
        dishes = await self.dish_repository.get_dishes(menu_id, submenu_id)
        result = []
        for dish in dishes:
            temp = {
                'id': str(dish.id),
                'title': dish.title,
                'description': dish.description,
                'price': str(dish.price)
            }
            result.append(temp)
        await DishRedis.set_dishes(menu_id, submenu_id, pickle.dumps(result))
        return result

    async def create_item(self, menu_id: int, submenu_id: int, dish_data: schemas.Dish,
                          background_tasks: BackgroundTasks) -> JSONResponse:
        new_dish = await self.dish_repository.create_dish(menu_id, submenu_id, dish_data)
        background_tasks.add_task(SubmenuRedis.clear_submenu_data, menu_id, submenu_id)
        background_tasks.add_task(DishRedis.delete_dishes, menu_id, submenu_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={'id': str(new_dish.id),
                                     'title': new_dish.title,
                                     'description': new_dish.description,
                                     'price': str(new_dish.price)})

    async def get_item(self, menu_id: int, submenu_id: int, dish_id: int) -> JSONResponse:
        dish_redis = await DishRedis.get_dish(menu_id, submenu_id, dish_id)
        if dish_redis:
            return pickle.loads(dish_redis)
        else:
            dish = await self.dish_repository.get_dish(menu_id, submenu_id, dish_id)
            await DishRedis.set_dish(menu_id, submenu_id, dish_id, pickle.dumps(dish))

        return JSONResponse(status_code=status.HTTP_200_OK, content={'id': str(dish.id),
                                                                     'title': dish.title,
                                                                     'description': dish.description,
                                                                     'price': str(dish.price)})

    async def update_item(self, menu_id: int, submenu_id: int, dish_id: int, dish_data: schemas.Dish,
                          background_tasks: BackgroundTasks) -> JSONResponse:
        dish_fromdb = await self.dish_repository.update_dish(menu_id, submenu_id, dish_id, dish_data)
        background_tasks.add_task(DishRedis.clear_dish_data, menu_id, submenu_id, dish_id)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'id': str(dish_fromdb.id),
                                     'title': dish_fromdb.title,
                                     'description': dish_fromdb.description,
                                     'price': str(dish_fromdb.price)})

    async def delete_item(self, menu_id: int, submenu_id: int, dish_id: int,
                          background_tasks: BackgroundTasks) -> JSONResponse:
        await self.dish_repository.delete_dish(menu_id, submenu_id, dish_id)
        background_tasks.add_task(DishRedis.clear_dish_data, menu_id, submenu_id, dish_id)
        return JSONResponse(status_code=200, content=[])
