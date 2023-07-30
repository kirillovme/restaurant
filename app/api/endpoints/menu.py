from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.api.models import models
from app.api.schemas import schemas
from app.database.database import get_db
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get('/menus')
def get_menus(db: Session = Depends(get_db)):
    menus = db.query(models.Menu).all()
    result = []
    for menu in menus:
        temp = {
            "id": str(menu.id),
            "title": menu.title,
            "description": menu.description,
            "submenus_count": db.query(models.Submenu).filter_by(menu_id=menu.id).count(),
            "dishes_count": db.query(models.Dish).join(models.Submenu).filter(models.Submenu.menu_id == menu.id).count()
        }
        result.append(temp)

    return result


@router.post('/menus')
def create_menu(menu: schemas.Menu, db: Session = Depends(get_db)):
    new_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": str(new_menu.id), "title": new_menu.title,
                                                                       "description": new_menu.description})


@router.get('/menus/{menu_id}')
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"id": str(menu.id),
                                 "title": menu.title,
                                 "description": menu.description,
                                 "submenus_count": db.query(models.Submenu).filter_by(menu_id=menu.id).count(),
                                 "dishes_count": (db.query(models.Dish)
                                                  .join(models.Submenu)
                                                  .filter(models.Submenu.menu_id == menu.id)
                                                  .count())})


@router.patch('/menus/{menu_id}')
def update_menu(menu_id: int, menu: schemas.Menu, db: Session = Depends(get_db)):
    menu_fromdb = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu_fromdb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    for key, value in menu.model_dump(exclude_unset=True).items():
        setattr(menu_fromdb, key, value)
    db.commit()
    db.refresh(menu_fromdb)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"id": str(menu_fromdb.id),
                                 "title": menu_fromdb.title,
                                 "description": menu_fromdb.description,
                                 "submenus_count": db.query(models.Submenu).filter_by(menu_id=menu_fromdb.id).count(),
                                 "dishes_count": (db.query(models.Dish)
                                                  .join(models.Submenu)
                                                  .filter(models.Submenu.menu_id == menu_fromdb.id)
                                                  .count())})


@router.delete('/menus/{menu_id}')
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_fromdb = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu_fromdb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    db.delete(menu_fromdb)
    db.commit()

    return JSONResponse(status_code=200, content=[])
