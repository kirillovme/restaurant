from app.redis.redis_client import redis_connect
from app.redis.menu_redis import MenuRedis


class SubmenuRedis:
    redis_connect = redis_connect

    @classmethod
    def set_submenus(cls, menu_id: int, data: bytes):
        cls.redis_connect.set("menu__" + str(menu_id) + "__submenus", data, get=True)

    @classmethod
    def get_submenus(cls, menu_id: int):
        return cls.redis_connect.get("menu__" + str(menu_id) + "__submenus")

    @classmethod
    def delete_submenus(cls, menu_id: int):
        return cls.redis_connect.delete("menu__" + str(menu_id) + "__submenus")

    @classmethod
    def set_submenu(cls, menu_id: int, submenu_id: int, data: bytes):
        cls.redis_connect.set("menu__" + str(menu_id) + "__submenus__" + str(submenu_id), data, get=True)

    @classmethod
    def get_submenu(cls, menu_id: int, submenu_id: int):
        return cls.redis_connect.get("menu__" + str(menu_id) + "__submenus__" + str(submenu_id))

    @classmethod
    def delete_submenu(cls, menu_id: int, submenu_id: int):
        cls.redis_connect.delete("menu__" + str(menu_id) + "__submenus__" + str(submenu_id))

    @classmethod
    def clear_submenu_data(cls, menu_id: int, submenu_id: int):
        MenuRedis.delete_menus()
        MenuRedis.delete_menu(menu_id)
        SubmenuRedis.delete_submenu(menu_id, submenu_id)
        SubmenuRedis.delete_submenus(menu_id)