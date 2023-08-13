from __future__ import annotations

from app.redis.menu_redis import MenuRedis
from app.redis.redis_client import redis_client


class SubmenuRedis:
    redis_client = redis_client

    @classmethod
    async def set_submenus(cls, menu_id: int, data: bytes) -> None:
        await cls.redis_client.redis_conn.set('menu__' + str(menu_id) + '__submenus', data)

    @classmethod
    async def get_submenus(cls, menu_id: int) -> bytes | None:
        return await cls.redis_client.redis_conn.get('menu__' + str(menu_id) + '__submenus')

    @classmethod
    async def delete_submenus(cls, menu_id: int) -> None:
        await cls.redis_client.redis_conn.delete('menu__' + str(menu_id) + '__submenus')

    @classmethod
    async def set_submenu(cls, menu_id: int, submenu_id: int, data: bytes) -> None:
        await cls.redis_client.redis_conn.set('menu__' + str(menu_id) + '__submenus__' + str(submenu_id), data)

    @classmethod
    async def get_submenu(cls, menu_id: int, submenu_id: int) -> bytes | None:
        return await cls.redis_client.redis_conn.get('menu__' + str(menu_id) + '__submenus__' + str(submenu_id))

    @classmethod
    async def delete_submenu(cls, menu_id: int, submenu_id: int) -> None:
        await cls.redis_client.redis_conn.delete('menu__' + str(menu_id) + '__submenus__' + str(submenu_id))

    @classmethod
    async def clear_submenu_data(cls, menu_id: int, submenu_id: int) -> None:
        await MenuRedis.clear_menu_data(menu_id)
        await SubmenuRedis.delete_submenu(menu_id, submenu_id)
        await SubmenuRedis.delete_submenus(menu_id)
