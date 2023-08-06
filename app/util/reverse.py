from app.api.endpoints import dish, menu, submenu
from app.main import app

# Dictionary of prefixes and routers
router_prefixes = {
    '/api/v1': menu.router,
    '/api/v1/menus/{menu_id}': submenu.router,
    '/api/v1/menus/{menu_id}/submenus/{submenu_id}': dish.router
}


def reverse(name: str, **path_params):
    for route in app.routes:
        if route.name == name:
            path = route.path_format.format(**path_params)
            for prefix_pattern, router in router_prefixes.items():
                if route in router.routes:
                    prefix = prefix_pattern.format(**path_params)
                    return prefix + path
            return path
    return None
