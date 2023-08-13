# Restaurant app
## Project description
This is a project of resturant app made during Ylab.

### API endpoints:

#### Menu:
> GET /api/v1/menus - Show all menus list

> GET /api/v1/menus/details - Show all menus list with submenus and dishes

> GET /api/v1/menus/{menu_id} - Show menu by id

> POST /api/v1/menus - Create menu

> PATCH /api/v1/menus/{menu_id} - Update menu by id

> DELETE /api/v1/menus/{menu_id} - Delete menu by id

#### Submenu:
> GET /api/v1/menus/{menu_id}/submenus - Get all submenus by menu_id

> GET /api/v1/menus/{menu_id}/submenus/{submenu_id} - Get submenu by menu_id and submenu_id

> POST /api/v1/menus/{menu_id}/submenus - Create submenu for menu_id

> PATCH /api/v1/menus/{menu_id}/submenus/{submenu_id} - Update submenu by menu_id and submenu_id

> DELETE /api/v1/menus/{menu_id}/submenus/{submenu_id} - Delete submenu by menu_id and submenu_id

#### Dish:
> GET /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes - Get dishes by menu_id and submenu_id

> GET /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - Get dish by menu_id, submenu_id, dish_id

> POST /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes - Create dish for submenu_id in menu_id

> PATCH /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - Update dish_id in submenu_id in menu_id

> DELETE /api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - Delete dish_id in submenu_id in menu_id


## How to run project:
### Run without Celery+RabbitMQ
1) docker-compose up -d
2) docker-compose up test

### Run with Celery+RabbitMQ
The tests will run right after the start of the project
1) docker-compose -f docker-compose-celery.yaml up -d


## Hard tasks completed:

1) ** Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest

Answer: app/api/tests/test_dishes_count.py

2) * Описать ручки API в соответствий c OpenAPI

Answer: app/api/endpoints

3) ** Реализовать в тестах аналог Django reverse() для FastAP

Answer: app/util/reverse.py
