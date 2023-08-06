from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.models import models
from app.api.schemas import schemas
from app.database.database import get_db


class MenuRepository:
    def __init__(self, session: Session = Depends(get_db)) -> None:
        self.session = session
        self.model = models.Menu

    def get_menus(self) -> list[models.Menu]:
        menus = self.session.query(models.Menu).all()
        return menus

    def create_menu(self, menu_data: schemas.Menu) -> models.Menu:
        new_menu = models.Menu(title=menu_data.title, description=menu_data.description)
        self.session.add(new_menu)
        self.session.commit()
        self.session.refresh(new_menu)
        return new_menu

    def get_menu(self, menu_id: int) -> models.Menu:
        menu = self.session.query(models.Menu).filter(models.Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='menu not found')
        return menu

    def update_menu(self, menu_id: int, menu_data: schemas.Menu) -> models.Menu:
        menu_fromdb = self.get_menu(menu_id)

        for key, value in menu_data.model_dump(exclude_unset=True).items():
            setattr(menu_fromdb, key, value)
        self.session.commit()
        self.session.refresh(menu_fromdb)
        return menu_fromdb

    def delete_menu(self, menu_id: int) -> None:
        menu_fromdb = self.get_menu(menu_id)

        self.session.delete(menu_fromdb)
        self.session.commit()

    def count_submenus(self, menu_id: int) -> int:
        return self.session.query(models.Submenu).filter_by(menu_id=menu_id).count()

    def count_dishes(self, menu_id: int) -> int:
        return self.session.query(models.Dish).join(models.Submenu).filter(
            models.Submenu.menu_id == menu_id).count()
