from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuResponse(Menu):
    id: str
    submenus_count: int
    dishes_count: int


class Submenu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SubmenuResponse(Submenu):
    id: str
    dishes_count: int


class DishBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Dish(DishBase):
    price: float


class DishResponse(DishBase):
    id: str
    price: str


class DishDetailedResponse(DishResponse):
    pass


class SubmenuDetailedResponse(Submenu):
    id: str
    dishes: list[DishDetailedResponse]


class MenuDetailedResponse(Menu):
    id: str
    submenus: list[SubmenuDetailedResponse]
