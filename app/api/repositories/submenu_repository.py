from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.models import models
from app.api.repositories.base_repository import BaseRepository
from app.api.repositories.menu_repository import MenuRepository
from app.api.schemas import schemas
from app.database.database import get_db


class SubmenuRepository(BaseRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)) -> None:
        super().__init__(session)
        self.model = models.Submenu
        self.menu_rep = MenuRepository(session)

    async def get_submenus(self, menu_id: int) -> list[models.Submenu]:
        menu = await self.menu_rep.get_menu(menu_id)
        return menu.submenus

    async def create_submenu(self, menu_id: int, submenu_data: schemas.Submenu) -> models.Submenu:
        menu = await self.menu_rep.get_menu(menu_id)
        new_submenu = models.Submenu(title=submenu_data.title, description=submenu_data.description, menu_id=menu.id)
        await self.db_add(new_submenu)
        return new_submenu

    async def get_submenu(self, menu_id: int, submenu_id: int) -> models.Submenu:
        result = await self.session.execute(
            select(self.model).
            where(self.model.id == submenu_id, self.model.menu_id == menu_id)
        )
        submenu = result.scalars().first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='submenu not found')

        return submenu

    async def update_submenu(self, menu_id: int, submenu_id: int, submenu_data: schemas.Submenu) -> models.Submenu:
        submenu_fromdb = await self.get_submenu(menu_id, submenu_id)
        for key, value in submenu_data.dict(exclude_unset=True).items():
            setattr(submenu_fromdb, key, value)
        await self.db_update(submenu_fromdb)
        return submenu_fromdb

    async def delete_submenu(self, menu_id: int, submenu_id: int) -> None:
        submenu_fromdb = await self.get_submenu(menu_id, submenu_id)

        await self.db_delete(submenu_fromdb)

    async def count_dishes(self, submenu_id: int) -> int:
        result = await self.session.execute(
            select(models.Dish).join(models.Submenu).filter(self.model.id == submenu_id)
        )
        return len(result.scalars().all())
