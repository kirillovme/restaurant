import pickle

from fastapi import BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse

from app.api.repositories.menu_repository import MenuRepository
from app.api.schemas import schemas
from app.redis.menu_redis import MenuRedis


class MenuService:

    def __init__(self, menu_repository: MenuRepository = Depends()) -> None:
        self.menu_repository = menu_repository

    async def create(self, menu_data: schemas.Menu, background_tasks: BackgroundTasks) -> JSONResponse:
        new_menu = await self.menu_repository.create_menu(menu_data)
        background_tasks.add_task(MenuRedis.clear_menus_data)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={'id': str(new_menu.id),
                                                                          'title': new_menu.title,
                                                                          'description': new_menu.description})

    async def get_items(self) -> list[dict]:
        menus_redis = await MenuRedis.get_menus()
        if menus_redis:
            return pickle.loads(menus_redis)
        menus = await self.menu_repository.get_menus()
        result = []
        for menu in menus:
            temp = {
                'id': str(menu.id),
                'title': menu.title,
                'description': menu.description,
                'submenus_count': await self.menu_repository.count_submenus(menu.id),
                'dishes_count': await self.menu_repository.count_dishes(menu.id)
            }
            result.append(temp)
        await MenuRedis.set_menus(pickle.dumps(result))
        return result

    async def get_items_details(self) -> list[dict]:
        menus = await self.menu_repository.get_menu_details()
        result = []
        for menu in menus:
            temp = {
                'id': str(menu.id),
                'title': menu.title,
                'description': menu.description,
                'submenus': [{
                    'id': str(submenu.id),
                    'title': submenu.title,
                    'description': submenu.description,
                    'dishes': [{
                        'id': str(dish.id),
                        'title': dish.title,
                        'description': dish.description,
                        'price': str(dish.price)
                    } for dish in submenu.dishes]
                } for submenu in menu.submenus]
            }
            result.append(temp)
        return result

    async def get_item(self, menu_id: int) -> JSONResponse:
        menu_redis = await MenuRedis.get_menu(menu_id)
        if menu_redis:
            menu = pickle.loads(menu_redis)
        else:
            menu = await self.menu_repository.get_menu(menu_id)
            await MenuRedis.set_menu(menu_id, pickle.dumps(menu))
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'id': str(menu.id),
                                     'title': menu.title,
                                     'description': menu.description,
                                     'submenus_count': await self.menu_repository.count_submenus(menu.id),
                                     'dishes_count': await self.menu_repository.count_dishes(menu.id)})

    async def update_item(self, menu_id: int, menu_data: schemas.Menu,
                          background_tasks: BackgroundTasks) -> JSONResponse:
        updated_menu = await self.menu_repository.update_menu(menu_id, menu_data)
        background_tasks.add_task(MenuRedis.clear_menu_data, menu_id)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'id': str(updated_menu.id),
                                     'title': updated_menu.title,
                                     'description': updated_menu.description,
                                     'submenus_count': await self.menu_repository.count_submenus(updated_menu.id),
                                     'dishes_count': await self.menu_repository.count_dishes(updated_menu.id)})

    async def delete_item(self, menu_id: int, background_tasks: BackgroundTasks) -> JSONResponse:
        await self.menu_repository.delete_menu(menu_id)
        background_tasks.add_task(MenuRedis.clear_menu_data, menu_id)
        return JSONResponse(status_code=200, content=[])
