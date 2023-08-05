from app.api.repositories.menu_repository import MenuRepository
from fastapi import Depends, status
from app.api.schemas import schemas
from fastapi.responses import JSONResponse
from app.redis.menu_redis import MenuRedis
import pickle


class MenuService:

    def __init__(self, menu_repository: MenuRepository = Depends()):
        self.menu_repository = menu_repository

    def create(self, menu_data: schemas.Menu) -> JSONResponse:
        new_menu = self.menu_repository.create_menu(menu_data)
        MenuRedis.delete_menus()
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(new_menu.id),
                                                                          "title": new_menu.title,
                                                                          "description": new_menu.description})

    def get_items(self) -> list[dict]:
        menus_redis = MenuRedis.get_menus()
        if menus_redis:
            return pickle.loads(menus_redis)
        menus = self.menu_repository.get_menus()
        result = []
        for menu in menus:
            temp = {
                "id": str(menu.id),
                "title": menu.title,
                "description": menu.description,
                "submenus_count": self.menu_repository.count_submenus(menu.id),
                "dishes_count": self.menu_repository.count_dishes(menu.id)
            }
            result.append(temp)
        MenuRedis.set_menus(pickle.dumps(result))
        return result

    def get_item(self, menu_id: int) -> JSONResponse:
        menu_redis = MenuRedis.get_menu(menu_id)
        if menu_redis:
            menu = pickle.loads(menu_redis)
        else:
            menu = self.menu_repository.get_menu(menu_id)
            MenuRedis.set_menu(menu_id, pickle.dumps(menu))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": str(menu.id),
                                     "title": menu.title,
                                     "description": menu.description,
                                     "submenus_count": self.menu_repository.count_submenus(menu.id),
                                     "dishes_count": self.menu_repository.count_dishes(menu.id)})

    def update_item(self, menu_id: int, menu_data: schemas.Menu) -> JSONResponse:
        updated_menu = self.menu_repository.update_menu(menu_id, menu_data)
        MenuRedis.clear_menu_data(menu_id)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": str(updated_menu.id),
                                     "title": updated_menu.title,
                                     "description": updated_menu.description,
                                     "submenus_count": self.menu_repository.count_submenus(updated_menu.id),
                                     "dishes_count": self.menu_repository.count_dishes(updated_menu.id)})

    def delete_item(self, menu_id: int) -> JSONResponse:
        self.menu_repository.delete_menu(menu_id)
        MenuRedis.clear_menu_data(menu_id)
        return JSONResponse(status_code=200, content=[])
