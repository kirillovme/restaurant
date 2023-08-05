from app.api.repositories.submenu_repository import SubmenuRepository
from fastapi import Depends, status
from app.api.schemas import schemas
from fastapi.responses import JSONResponse
from app.redis.submenu_redis import SubmenuRedis
from app.redis.menu_redis import MenuRedis
import pickle


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository = Depends()):
        self.submenu_repository = submenu_repository

    def get_items(self, menu_id: int) -> list[dict]:
        submenus_redis = SubmenuRedis.get_submenus(menu_id)
        if submenus_redis:
            return pickle.loads(submenus_redis)
        submenus = self.submenu_repository.get_submenus(menu_id)
        result = []
        for submenu in submenus:
            temp = {
                "id": str(submenu.id),
                "title": submenu.title,
                "description": submenu.description,
                "dishes_count": self.submenu_repository.count_dishes(submenu.id)
            }
            result.append(temp)
        SubmenuRedis.set_submenus(menu_id, pickle.dumps(result))
        return result

    def create_item(self, menu_id: int, submenu_data: schemas.Submenu) -> JSONResponse:
        new_submenu = self.submenu_repository.create_submenu(menu_id, submenu_data)
        MenuRedis.delete_menus()
        MenuRedis.delete_menu(menu_id)
        SubmenuRedis.delete_submenus(menu_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={"id": str(new_submenu.id), "title": new_submenu.title,
                                     "description": new_submenu.description})

    def get_item(self, menu_id: int, submenu_id: int) -> JSONResponse:
        submenu_redis = SubmenuRedis.get_submenu(menu_id, submenu_id)
        if submenu_redis:
            submenu = pickle.loads(submenu_redis)
        else:
            submenu = self.submenu_repository.get_submenu(menu_id, submenu_id)
            SubmenuRedis.set_submenu(menu_id, submenu_id, pickle.dumps(submenu))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": str(submenu.id),
                                     "title": submenu.title,
                                     "description": submenu.description,
                                     "dishes_count": self.submenu_repository.count_dishes(submenu.id)})

    def update_item(self, menu_id: int, submenu_id: int, submenu_data: schemas.Submenu) -> JSONResponse:
        submenu_fromdb = self.submenu_repository.update_submenu(menu_id, submenu_id, submenu_data)
        SubmenuRedis.clear_submenu_data(menu_id, submenu_id)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={"id": str(submenu_fromdb.id),
                                     "title": submenu_fromdb.title,
                                     "description": submenu_fromdb.description,
                                     "dishes_count": self.submenu_repository.count_dishes(submenu_fromdb.id)})

    def delete_item(self, menu_id: int, submenu_id: int) -> JSONResponse:
        self.submenu_repository.delete_submenu(menu_id, submenu_id)
        SubmenuRedis.clear_submenu_data(menu_id, submenu_id)
        return JSONResponse(status_code=200, content=[])
