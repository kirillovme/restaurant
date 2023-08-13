from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.api.models import models
from app.api.repositories.base_repository import BaseRepository
from app.api.schemas import schemas
from app.database.database import get_db


class MenuRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        super().__init__(session)
        self.model = models.Menu

    async def get_menus(self) -> list[models.Menu]:
        menus = await self.session.execute(select(self.model))
        return menus.scalars().all()

    async def create_menu(self, menu_data: schemas.Menu) -> models.Menu:
        new_menu = models.Menu(title=menu_data.title, description=menu_data.description)
        await self.db_add(new_menu)
        return new_menu

    async def get_menu(self, menu_id: int) -> models.Menu:
        result = await self.session.execute(
            select(self.model).where(self.model.id == menu_id)
        )
        menu = result.scalars().first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        return menu

    async def get_menu_details(self) -> list[models.Menu]:
        menus = await self.session.execute(
            select(self.model)
            .options(
                joinedload(models.Menu.submenus)
                .joinedload(models.Submenu.dishes)
            )
        )
        return menus.scalars().unique().all()

    async def update_menu(self, menu_id: int, menu_data: schemas.Menu) -> models.Menu:
        menu_fromdb = await self.get_menu(menu_id)
        for key, value in menu_data.dict(exclude_unset=True).items():
            setattr(menu_fromdb, key, value)
        await self.db_update(menu_fromdb)
        return menu_fromdb

    async def delete_menu(self, menu_id: int) -> None:
        menu_fromdb = await self.get_menu(menu_id)
        await self.db_delete(menu_fromdb)

    async def count_submenus(self, menu_id: int) -> int:
        result = await self.session.execute(
            select(models.Submenu).filter_by(menu_id=menu_id)
        )
        return len(result.scalars().all())

    async def count_dishes(self, menu_id: int) -> int:
        result = await self.session.execute(
            select(models.Dish).join(models.Submenu).filter(models.Submenu.menu_id == menu_id)
        )
        return len(result.scalars().all())
