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
        for menu in menus:
            menu_id = menu['id']
            response = await client.get(f'{BASE_URL}/menus/{menu_id}')
            if response.status_code == 200:
                menu_id = menu['id']
                del menu['id']
                await client.patch(f'{BASE_URL}/menus/{menu_id}', json=menu)
            elif response.status_code == 404:
                await client.post(f'{BASE_URL}/menus', json=menu)

        for submenu in submenus:
            submenu_id = submenu['id']
            menu_id = submenu['menu_id']
            response = await client.get(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}')

            if response.status_code == 200:
                del submenu['id']
                del submenu['menu_id']
                await client.patch(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}', json=submenu)
            elif response.status_code == 404:
                del submenu['menu_id']
                del submenu['id']
                await client.post(f'{BASE_URL}/menus/{menu_id}/submenus', json=submenu)

        for dish in dishes:
            dish_id = dish['id']
            submenu_id = dish['submenu_id']
            menu_id = dish['menu_id']
            response = await client.get(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')

            if response.status_code == 200:
                del dish['id']
                del dish['submenu_id']
                del dish['menu_id']
                await client.patch(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
                                   json=dish)
            elif response.status_code == 404:
                del dish['menu_id']
                del dish['submenu_id']
                await client.post(f'{BASE_URL}/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)
