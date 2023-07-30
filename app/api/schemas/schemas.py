from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Submenu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Dish(BaseModel):
    title: str
    description: str
    price: float

    class Config:
        orm_mode = True
