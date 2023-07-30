from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.api.models import models
from app.api.schemas import schemas
from app.database.database import get_db
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get('/dishes')
def get_dishes(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                              models.Submenu.menu_id == menu_id).first()
    if not submenu:
        return []
    return submenu.dishes


@router.post('/dishes')
def create_dish(menu_id: int, submenu_id: int, dish: schemas.Dish, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                              models.Submenu.menu_id == menu_id).first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    new_dish = models.Dish(title=dish.title, description=dish.description, price=dish.price, submenu_id=submenu.id)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"id": str(new_dish.id), "title": new_dish.title,
                                 "description": new_dish.description, "price": str(new_dish.price)})


@router.get('/dishes/{dish_id}')
def get_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    dish = (
        db.query(models.Dish)
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

    return JSONResponse(status_code=status.HTTP_200_OK, content={"id": str(dish.id), "title": dish.title,
                                                                 "description": dish.description,
                                                                 "price": str(dish.price)})


@router.patch('/dishes/{dish_id}')
def update_dish(menu_id: int, submenu_id: int, dish_id: int, dish: schemas.Dish, db: Session = Depends(get_db)):
    dish_fromdb = (
        db.query(models.Dish)
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

    for key, value in dish.model_dump(exclude_unset=True).items():
        setattr(dish_fromdb, key, value)

    db.commit()
    db.refresh(dish_fromdb)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"id": str(dish_fromdb.id), "title": dish_fromdb.title,
                                                                 "description": dish_fromdb.description,
                                                                 "price": str(dish_fromdb.price)})


@router.delete('/dishes/{dish_id}')
def delete_dish(menu_id: int, submenu_id: int, dish_id: int, db: Session = Depends(get_db)):
    dish = (
        db.query(models.Dish)
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

    db.delete(dish)
    db.commit()

    return JSONResponse(status_code=200, content=[])
