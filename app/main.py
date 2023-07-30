from fastapi import FastAPI
from app.api.endpoints import dish, menu, submenu

app = FastAPI()
app.include_router(menu.router, tags=['Menu'], prefix='/api/v1')
app.include_router(submenu.router, tags=['Submenu'], prefix='/api/v1/menus/{menu_id}')
app.include_router(dish.router, tags=['Dishes'], prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}')
