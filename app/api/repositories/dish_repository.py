from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException
from app.database.database import get_db
from app.api.models import models
from app.api.schemas import schemas
from app.api.repositories.submenu_repository import SubmenuRepository


class DishRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session
        self.model = models.Dish
        self.submenu_rep = SubmenuRepository(session)

    def get_dishes(self, menu_id: int, submenu_id: int) -> list[models.Dish]:
        submenu = self.session.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                                            models.Submenu.menu_id == menu_id).first()
        if not submenu:
            return []

        return submenu.dishes

    def create_dish(self, menu_id: int, submenu_id: int, dish_data: schemas.Dish) -> models.Dish:
        submenu = self.submenu_rep.get_submenu(menu_id, submenu_id)
        new_dish = models.Dish(title=dish_data.title,
                               description=dish_data.description,
                               price=dish_data.price,
                               submenu_id=submenu.id)
        self.session.add(new_dish)
        self.session.commit()
        self.session.refresh(new_dish)
        return new_dish

    def get_dish(self, menu_id: int, submenu_id: int, dish_id: int) -> models.Dish:
        dish = (
            self.session.query(models.Dish)
            .join(models.Submenu)
            .join(models.Menu)
            .filter(
                models.Dish.id == dish_id,
                models.Submenu.id == submenu_id,
                models.Menu.id == menu_id
            ).first()
        )
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

        return dish

    def update_dish(self, menu_id: int, submenu_id: int, dish_id: int, dish_data: schemas.Dish) -> models.Dish:
        dish_fromdb = (
            self.session.query(models.Dish)
            .join(models.Submenu)
            .join(models.Menu)
            .filter(
                models.Dish.id == dish_id,
                models.Submenu.id == submenu_id,
                models.Menu.id == menu_id
            ).first()
        )
        if not dish_fromdb:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

        for key, value in dish_data.model_dump(exclude_unset=True).items():
            setattr(dish_fromdb, key, value)

        self.session.commit()
        self.session.refresh(dish_fromdb)

        return dish_fromdb

    def delete_dish(self, menu_id: int, submenu_id: int, dish_id: int):
        dish = (
            self.session.query(models.Dish)
            .join(models.Submenu)
            .join(models.Menu)
            .filter(
                models.Dish.id == dish_id,
                models.Submenu.id == submenu_id,
                models.Menu.id == menu_id
            ).first()
        )
        if not dish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")

        self.session.delete(dish)
        self.session.commit()
