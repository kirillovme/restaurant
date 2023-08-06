from __future__ import annotations

from app.redis.redis_client import redis_connect


class MenuRedis:
    redis_connect = redis_connect

    @classmethod
    def set_menus(cls, data: bytes) -> None:
        cls.redis_connect.set('menus', data, get=True)

    @classmethod
    def delete_menus(cls) -> None:
        cls.redis_connect.delete('menus')

    @classmethod
    def get_menus(cls) -> bytes | None:
        return cls.redis_connect.get('menus')

    @classmethod
    def set_menu(cls, menu_id: int, data: bytes) -> None:
        cls.redis_connect.set('menu__' + str(menu_id), data, get=True)

    @classmethod
    def get_menu(cls, menu_id: int) -> bytes | None:
        return cls.redis_connect.get('menu__' + str(menu_id))

    @classmethod
    def delete_menu(cls, menu_id: int) -> None:
        cls.redis_connect.delete('menu__' + str(menu_id))

    @classmethod
    def clear_menu_data(cls, menu_id: int) -> None:
        MenuRedis.delete_menus()
        MenuRedis.delete_menu(menu_id)
