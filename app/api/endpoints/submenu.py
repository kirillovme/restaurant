from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.api.models import models
from app.api.schemas import schemas
from app.database.database import get_db
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get('/submenus')
def get_submenus(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")

    result = []
    for submenu in menu.submenus:
        temp = {
            "id": str(submenu.id),
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": db.query(models.Dish).join(models.Submenu).filter(models.Submenu.id == submenu.id).count()
        }
        result.append(temp)
    return result


@router.post('/submenus')
def create_submenu(menu_id: int, submenu: schemas.Submenu, db: Session = Depends(get_db)):
    menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="menu not found")
    new_submenu = models.Submenu(title=submenu.title, description=submenu.description, menu_id=menu.id)
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"id": str(new_submenu.id), "title": new_submenu.title,
                                 "description": new_submenu.description})


@router.get('/submenus/{submenu_id}')
def get_submenu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                              models.Submenu.menu_id == menu_id).first()
    if not submenu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"id": str(submenu.id),
                                 "title": submenu.title,
                                 "description": submenu.description,
                                 "dishes_count": (db.query(models.Dish)
                                                  .join(models.Submenu)
                                                  .filter(models.Submenu.id == submenu.id)
                                                  .count())})


@router.patch('/submenus/{submenu_id}')
def update_menu(menu_id: int, submenu_id: int, submenu: schemas.Submenu, db: Session = Depends(get_db)):
    submenu_fromdb = db.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                                     models.Submenu.menu_id == menu_id).first()
    if not submenu_fromdb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    for key, value in submenu.model_dump(exclude_unset=True).items():
        setattr(submenu_fromdb, key, value)
    db.commit()
    db.refresh(submenu_fromdb)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"id": str(submenu_fromdb.id),
                                 "title": submenu_fromdb.title,
                                 "description": submenu_fromdb.description,
                                 "dishes_count": (db.query(models.Dish)
                                                  .join(models.Submenu)
                                                  .filter(models.Submenu.id == submenu_fromdb.id)
                                                  .count())})


@router.delete('/submenus/{submenu_id}')
def delete_menu(menu_id: int, submenu_id: int, db: Session = Depends(get_db)):
    submenu_fromdb = db.query(models.Submenu).filter(models.Submenu.id == submenu_id,
                                                     models.Submenu.menu_id == menu_id).first()
    if not submenu_fromdb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")

    db.delete(submenu_fromdb)
    db.commit()

    return JSONResponse(status_code=200, content=[])
