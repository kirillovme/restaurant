from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import models
from app.api.repositories.base_repository import BaseRepository
from app.api.repositories.submenu_repository import SubmenuRepository
from app.api.schemas import schemas
from app.database.database import get_db


class DishRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        super().__init__(session)
        self.model = models.Dish
        self.submenu_rep = SubmenuRepository(session)

    async def get_dishes(self, menu_id: int, submenu_id: int) -> list[models.Dish]:
        result = await self.session.execute(
            select(models.Submenu).
            where(models.Submenu.id == submenu_id, models.Submenu.menu_id == menu_id)
        )
        submenu = result.scalars().first()
        if not submenu:
            return []

        return submenu.dishes

    async def create_dish(self, menu_id: int, submenu_id: int, dish_data: schemas.Dish) -> models.Dish:
        submenu = await self.submenu_rep.get_submenu(menu_id, submenu_id)
        new_dish = models.Dish(title=dish_data.title,
                               description=dish_data.description,
                               price=dish_data.price,
                               submenu_id=submenu.id)
        await self.db_add(new_dish)
        return new_dish

    async def get_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> models.Dish:
        result = await self.session.execute(
            select(self.model)
            .join(models.Submenu)
            .join(models.Menu)
            .filter(
                models.Dish.id == dish_id,
                models.Submenu.id == submenu_id,
                models.Menu.id == menu_id
            )
        )

        dish = result.scalars().first()
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='dish not found')

        return dish

    async def update_dish(self, menu_id: int, submenu_id: int, dish_id: int, dish_data: schemas.Dish) -> models.Dish:
        dish = await self.get_dish(menu_id, submenu_id, dish_id)

        for key, value in dish_data.dict(exclude_unset=True).items():
            setattr(dish, key, value)

        await self.db_update(dish)

        return dish

    async def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> None:
        dish = await self.get_dish(menu_id, submenu_id, dish_id)
        await self.db_delete(dish)
