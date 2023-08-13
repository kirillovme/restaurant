from fastapi import FastAPI

from app.api.endpoints import dish, menu, submenu
from app.redis.redis_client import redis_client

app = FastAPI()
app.include_router(menu.router, tags=['Menus'], prefix='/api/v1')
app.include_router(submenu.router, tags=['Submenus'], prefix='/api/v1/menus/{menu_id}')
app.include_router(dish.router, tags=['Dishes'], prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}')


@app.on_event('startup')
async def create_event() -> None:
    await redis_client.setup()


@app.on_event('shutdown')
async def shutdown_event() -> None:
    await redis_client.clear_cache()
