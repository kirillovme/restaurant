from app.api.repositories.dish_repository import DishRepository
from fastapi import Depends, status
from app.api.schemas import schemas
from fastapi.responses import JSONResponse
from app.redis.dish_redis import DishRedis
from app.redis.submenu_redis import SubmenuRedis
import pickle


class DishService:
    def __init__(self, dish_repository: DishRepository = Depends()):
        self.dish_repository = dish_repository

    def get_items(self, menu_id: int, submenu_id: int):
        dish_redis = DishRedis.get_dishes(menu_id, submenu_id)
        if dish_redis:
            return pickle.loads(dish_redis)
        dish = self.dish_repository.get_dishes(menu_id, submenu_id)
        DishRedis.set_dishes(menu_id, submenu_id, pickle.dumps(dish))
        return dish

    def create_item(self, menu_id: int, submenu_id: int, dish_data: schemas.Dish):
        new_dish = self.dish_repository.create_dish(menu_id, submenu_id, dish_data)
        SubmenuRedis.clear_submenu_data(menu_id, submenu_id)
        DishRedis.delete_dishes(menu_id, submenu_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"id": str(new_dish.id),
                                     "title": new_dish.title,
                                     "description": new_dish.description,
                                     "price": str(new_dish.price)})

    def get_item(self, menu_id: int, submenu_id: int, dish_id: int):
        dish_redis = DishRedis.get_dish(menu_id, submenu_id, dish_id)
        if dish_redis:
            return pickle.loads(dish_redis)
        else:
            dish = self.dish_repository.get_dish(menu_id, submenu_id, dish_id)
            DishRedis.set_dish(menu_id, submenu_id, dish_id, pickle.dumps(dish))

        return JSONResponse(status_code=status.HTTP_200_OK, content={"id": str(dish.id),
                                                                     "title": dish.title,
                                                                     "description": dish.description,
                                                                     "price": str(dish.price)})

    def update_item(self, menu_id: int, submenu_id: int, dish_id: int, dish_data: schemas.Dish):
        dish_fromdb = self.dish_repository.update_dish(menu_id, submenu_id, dish_id, dish_data)
        DishRedis.clear_dish_data(menu_id, submenu_id, dish_id)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": str(dish_fromdb.id),
                                     "title": dish_fromdb.title,
                                     "description": dish_fromdb.description,
                                     "price": str(dish_fromdb.price)})

    def delete_item(self, menu_id: int, submenu_id: int, dish_id: int):
        self.dish_repository.delete_dish(menu_id, submenu_id, dish_id)
        DishRedis.clear_dish_data(menu_id, submenu_id, dish_id)
        return JSONResponse(status_code=200, content=[])
