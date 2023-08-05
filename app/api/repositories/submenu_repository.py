from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from app.database.database import get_db
from app.api.models import models
from app.api.schemas import schemas
from app.api.repositories.menu_repository import MenuRepository


class SubmenuRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.model = models.Submenu
        self.menu_rep = MenuRepository(session)

    def get_submenus(self, menu_id: int) -> list[models.Submenu]:
        menu = self.menu_rep.get_menu(menu_id)
        return menu.submenus

    def create_submenu(self, menu_id: int, submenu_data: schemas.Submenu) -> models.Submenu:
        menu = self.menu_rep.get_menu(menu_id)
        new_submenu = models.Submenu(title=submenu_data.title, description=submenu_data.description, menu_id=menu.id)
        self.session.add(new_submenu)
        self.session.commit()
        self.session.refresh(new_submenu)
        return new_submenu

    def get_submenu(self, menu_id: int, submenu_id: int) -> models.Submenu:
        submenu = self.session.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                                            models.Submenu.menu_id == menu_id).first()
        if not submenu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

        return submenu

    def update_submenu(self, menu_id: int, submenu_id: int, submenu_data: schemas.Submenu) -> models.Submenu:
        submenu_fromdb = self.session.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                                                   models.Submenu.menu_id == menu_id).first()
        if not submenu_fromdb:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

        for key, value in submenu_data.model_dump(exclude_unset=True).items():
            setattr(submenu_fromdb, key, value)
        self.session.commit()
        self.session.refresh(submenu_fromdb)
        return submenu_fromdb

    def delete_submenu(self, menu_id: int, submenu_id: int):
        submenu_fromdb = self.session.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                                                   models.Submenu.menu_id == menu_id).first()
        if not submenu_fromdb:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

        self.session.delete(submenu_fromdb)
        self.session.commit()

    def count_dishes(self, submenu_id: int) -> int:
        return self.session.query(models.Dish).join(models.Submenu).filter(
            models.Submenu.id == submenu_id).count()
