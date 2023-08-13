from __future__ import annotations

from app.redis.redis_client import redis_client
from app.redis.submenu_redis import SubmenuRedis


class DishRedis:
    redis_client = redis_client

    @classmethod
    async def set_dishes(cls, menu_id: int, submenu_id: int, data: bytes) -> None:
        await cls.redis_client.redis_conn.set('menu__' + str(menu_id) + '__submenus__' + str(submenu_id) + '__dishes', data)

    @classmethod
    async def get_dishes(cls, menu_id: int, submenu_id: int) -> bytes | None:
        return await cls.redis_client.redis_conn.get('menu__' + str(menu_id) + '__submenus__' + str(submenu_id) + '__dishes')

    @classmethod
    async def delete_dishes(cls, menu_id: int, submenu_id: int) -> None:
        await cls.redis_client.redis_conn.delete('menu__' + str(menu_id) + '__submenus__' + str(submenu_id) + '__dishes')

    @classmethod
    async def set_dish(cls, menu_id: int, submenu_id: int, dish_id: int, data: bytes) -> None:
        await cls.redis_client.redis_conn.\
            set('menu__' + str(menu_id) + '__submenus__' + str(submenu_id) + '__dishes__' + str(dish_id), data)

    @classmethod
    async def get_dish(cls, menu_id: int, submenu_id: int, dish_id: int) -> bytes | None:
        return await cls.redis_client.redis_conn.\
            get('menu__' + str(menu_id) + '__submenus__' + str(submenu_id) + '__dishes__' + str(dish_id))

    @classmethod
    async def delete_dish(cls, menu_id: int, submenu_id: int, dish_id: int) -> None:
        await cls.redis_client.redis_conn.\
            delete('menu__' + str(menu_id) + '__submenus__' + str(submenu_id) + '__dishes__' + str(dish_id))

    @classmethod
    async def clear_dish_data(cls, menu_id: int, submenu_id: int, dish_id: int) -> None:
        await SubmenuRedis.clear_submenu_data(menu_id, submenu_id)
        await DishRedis.delete_dish(menu_id, submenu_id, dish_id)
        await DishRedis.delete_dishes(menu_id, submenu_id)
