import asyncio
import os
from datetime import timedelta

import pandas as pd
from celery import Celery
from httpx import AsyncClient

from app.util.parse_admin import parse_excel_data

celery_app = Celery('tasks')

file_path = os.path.join(os.path.dirname(__file__), '..', 'admin', 'Menu.xlsx')

celery_app.conf.broker_url = 'amqp://guest:guest@rabbitmq:5672//'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.broker_connection_retry_on_startup = True

celery_app.conf.beat_schedule = {
    'database_sync': {
        'task': 'app.tasks.celery_worker.database_sync',
        'schedule': timedelta(seconds=15),
    },
}


def read_and_parse(filepath):
    df = pd.read_excel(filepath, header=None)
    menus, submenus, dishes = parse_excel_data(df)
    return menus, submenus, dishes


@celery_app.task
def database_sync():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    menus, submenus, dishes = read_and_parse('https://docs.google.com/spreadsheets/d'
                                             '/1On2gNZyWVnUyvcvUljG6qv4xCqOZPIlRAoVlva58zGw/export?format=xlsx')
    loop.run_until_complete(async_database_operations(menus, submenus, dishes))
    loop.close()


BASE_URL = 'http://app:8000/api/v1'


async def async_database_operations(menus, submenus, dishes):
    async with AsyncClient() as client:
        # Fetch existing records
        db_menus = await fetch_all_from_database(client, '/menus')
        db_submenus = {menu_id: await fetch_all_from_database(client, f'/menus/{menu_id}/submenus') for menu_id in
                       db_menus.keys()}
        db_dishes = {}
        for submenu in submenus:
            submenu_id = str(submenu['id'])
            menu_id = str(submenu['menu_id'])
            endpoint = f'/menus/{menu_id}/submenus/{submenu_id}/dishes'
            db_dishes[submenu_id] = await fetch_all_from_database(client, endpoint)

        # Synchronize menus
        for menu in menus:
            menu_id = str(menu['id'])
            if menu_id in db_menus:
                del db_menus[menu_id]
                await client.patch(f'{BASE_URL}/menus/{menu_id}', json=menu)
            else:
                await client.post(f'{BASE_URL}/menus', json=menu)
        for menu_id in db_menus.keys():
            await client.delete(f'{BASE_URL}/menus/{menu_id}')

        # Synchronize submenus
        for submenu in submenus:
            submenu_id = str(submenu['id'])
            menu_id = str(submenu['menu_id'])
            if submenu_id in db_submenus.get(menu_id, {}):
                del db_submenus[menu_id][submenu_id]
                await client.patch(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}', json=submenu)
            else:
                await client.post(f'{BASE_URL}/menus/{menu_id}/submenus', json=submenu)
        for menu_id, submenu_dict in db_submenus.items():
            for submenu_id in submenu_dict.keys():
                await client.delete(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}')

        # Synchronize dishes
        for dish in dishes:
            dish_id = str(dish['id'])
            submenu_id = str(dish['submenu_id'])
            menu_id = str(dish['menu_id'])
            if dish_id in db_dishes.get(submenu_id, {}):
                del db_dishes[submenu_id][dish_id]
                await client.patch(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json=dish)
            else:
                await client.post(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)

        for submenu_id, dishes_dict in db_dishes.items():
            menu_id = next((submenu['menu_id'] for submenu in submenus if str(submenu['id']) == submenu_id), None)
            for dish_id in dishes_dict.keys():
                await client.delete(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')


async def fetch_all_from_database(client, endpoint):
    response = await client.get(f'{BASE_URL}{endpoint}')
    if response.status_code == 200:
        return {str(item['id']): item for item in response.json()}
    return {}
