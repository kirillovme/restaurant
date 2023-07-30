from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.database.database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    submenus = relationship("Submenu", cascade='all, delete', back_populates="menu")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    title = Column(String)
    description = Column(String)

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", cascade='all, delete', back_populates="submenu")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    submenu_id = Column(Integer, ForeignKey("submenus.id"))
    title = Column(String)
    description = Column(String)
    price = Column(Numeric(10, 2))

    submenu = relationship("Submenu", back_populates="dishes")
