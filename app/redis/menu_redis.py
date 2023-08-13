from __future__ import annotations

from app.redis.redis_client import redis_client


class MenuRedis:
    redis_client = redis_client

    @classmethod
    async def set_menus_details(cls, data: bytes) -> None:
        await cls.redis_client.redis_conn.set('menus_details', data)

    @classmethod
    async def delete_menus_details(cls) -> None:
        await cls.redis_client.redis_conn.delete('menus_details')

    @classmethod
    async def get_menus_details(cls) -> bytes | None:
        return await cls.redis_client.redis_conn.get('menus_details')

    @classmethod
    async def set_menus(cls, data: bytes) -> None:
        await cls.redis_client.redis_conn.set('menus', data)

    @classmethod
    async def delete_menus(cls) -> None:
        await cls.redis_client.redis_conn.delete('menus')

    @classmethod
    async def get_menus(cls) -> bytes | None:
        return await cls.redis_client.redis_conn.get('menus')

    @classmethod
    async def set_menu(cls, menu_id: int, data: bytes) -> None:
        await cls.redis_client.redis_conn.set('menu__' + str(menu_id), data)

    @classmethod
    async def get_menu(cls, menu_id: int) -> bytes | None:
        return await cls.redis_client.redis_conn.get('menu__' + str(menu_id))

    @classmethod
    async def delete_menu(cls, menu_id: int) -> None:
        await cls.redis_client.redis_conn.delete('menu__' + str(menu_id))

    @classmethod
    async def clear_menus_data(cls) -> None:
        await MenuRedis.delete_menus()
        await MenuRedis.delete_menus_details()

    @classmethod
    async def clear_menu_data(cls, menu_id: int) -> None:
        await MenuRedis.delete_menus()
        await MenuRedis.delete_menu(menu_id)
        await MenuRedis.delete_menus_details()
