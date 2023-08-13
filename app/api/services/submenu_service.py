import pickle

from fastapi import BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from app.api.repositories.submenu_repository import SubmenuRepository
from app.api.schemas import schemas
from app.redis.menu_redis import MenuRedis
from app.redis.submenu_redis import SubmenuRedis


class SubmenuService:
    def __init__(self, submenu_repository: SubmenuRepository = Depends()) -> None:
        self.submenu_repository = submenu_repository

    async def get_items(self, menu_id: int) -> list[dict]:
        submenus_redis = await SubmenuRedis.get_submenus(menu_id)
        if submenus_redis:
            return pickle.loads(submenus_redis)
        submenus = await self.submenu_repository.get_submenus(menu_id)
        result = []
        for submenu in submenus:
            temp = {
                'id': str(submenu.id),
                'title': submenu.title,
                'description': submenu.description,
                'dishes_count': await self.submenu_repository.count_dishes(submenu.id)
            }
            result.append(temp)
        await SubmenuRedis.set_submenus(menu_id, pickle.dumps(result))
        return result

    async def create_item(self, menu_id: int, submenu_data: schemas.Submenu,
                          background_tasks: BackgroundTasks) -> JSONResponse:
        new_submenu = await self.submenu_repository.create_submenu(menu_id, submenu_data)
        background_tasks.add_task(MenuRedis.clear_menu_data, menu_id)
        background_tasks.add_task(SubmenuRedis.delete_submenus, menu_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={'id': str(new_submenu.id), 'title': new_submenu.title,
                                     'description': new_submenu.description})

    async def get_item(self, menu_id: int, submenu_id: int) -> JSONResponse:
        submenu_redis = await SubmenuRedis.get_submenu(menu_id, submenu_id)
        if submenu_redis:
            submenu = pickle.loads(submenu_redis)
        else:
            submenu = await self.submenu_repository.get_submenu(menu_id, submenu_id)
            await SubmenuRedis.set_submenu(menu_id, submenu_id, pickle.dumps(submenu))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'id': str(submenu.id),
                                     'title': submenu.title,
                                     'description': submenu.description,
                                     'dishes_count': await self.submenu_repository.count_dishes(submenu.id)})

    async def update_item(self, menu_id: int, submenu_id: int, submenu_data: schemas.Submenu,
                          background_tasks: BackgroundTasks) -> JSONResponse:
        submenu_fromdb = await self.submenu_repository.update_submenu(menu_id, submenu_id, submenu_data)
        background_tasks.add_task(SubmenuRedis.clear_submenu_data, menu_id, submenu_id)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'id': str(submenu_fromdb.id),
                                     'title': submenu_fromdb.title,
                                     'description': submenu_fromdb.description,
                                     'dishes_count': await self.submenu_repository.count_dishes(submenu_fromdb.id)})

    async def delete_item(self, menu_id: int, submenu_id: int,
                          background_tasks: BackgroundTasks) -> JSONResponse:
        await self.submenu_repository.delete_submenu(menu_id, submenu_id)
        background_tasks.add_task(SubmenuRedis.clear_submenu_data, menu_id, submenu_id)
        return JSONResponse(status_code=200, content=[])
