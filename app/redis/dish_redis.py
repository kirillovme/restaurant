from app.redis.redis_client import redis_connect
from app.redis.submenu_redis import SubmenuRedis


class DishRedis:
    redis_connect = redis_connect

    @classmethod
    def set_dishes(cls, menu_id: int, submenu_id: int, data: bytes):
        cls.redis_connect.set("menu__" + str(menu_id) + "__submenus__" + str(submenu_id) + "__dishes", data, get=True)

    @classmethod
    def get_dishes(cls, menu_id: int, submenu_id: int):
        return cls.redis_connect.get("menu__" + str(menu_id) + "__submenus__" + str(submenu_id) + "__dishes")

    @classmethod
    def delete_dishes(cls, menu_id: int, submenu_id: int):
        return cls.redis_connect.delete("menu__" + str(menu_id) + "__submenus__" + str(submenu_id) + "__dishes")

    @classmethod
    def set_dish(cls, menu_id: int, submenu_id: int, dish_id: int, data: bytes):
        return cls.redis_connect.set("menu__" + str(menu_id) + "__submenus__" + str(submenu_id) + "__dishes__"
                                     + str(dish_id), data)

    @classmethod
    def get_dish(cls, menu_id: int, submenu_id: int, dish_id: int):
        return cls.redis_connect.get("menu__" + str(menu_id) + "__submenus__" + str(submenu_id) + "__dishes__"
                                     + str(dish_id))

    @classmethod
    def delete_dish(cls, menu_id: int, submenu_id: int, dish_id: int):
        return cls.redis_connect.delete("menu__" + str(menu_id) + "__submenus__" + str(submenu_id) + "__dishes__"
                                        + str(dish_id))

    @classmethod
    def clear_dish_data(cls, menu_id: int, submenu_id: int, dish_id: int):
        SubmenuRedis.clear_submenu_data(menu_id, submenu_id)
        DishRedis.delete_dish(menu_id, submenu_id, dish_id)
        DishRedis.delete_dishes(menu_id, submenu_id)
