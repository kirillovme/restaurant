import pandas as pd


def parse_excel_data(df):
    menus = []
    submenus = []
    dishes = []

    current_menu = None
    current_submenu = None

    for _, row in df.iterrows():
        # Check for Menu record
        if not pd.isna(row[df.columns[0]]):
            current_menu = {
                'id': int(row[df.columns[0]]),
                'title': row[df.columns[1]],
                'description': row[df.columns[2]]
            }
            menus.append(current_menu)

            # Reset current_submenu as we've moved to a new menu
            current_submenu = None

        # Check for Submenu record
        elif not pd.isna(row[df.columns[1]]) and current_menu:
            current_submenu = {
                'id': int(row[df.columns[1]]),
                'menu_id': current_menu['id'],
                'title': row[df.columns[2]],
                'description': row[df.columns[3]]
            }
            submenus.append(current_submenu)

        # Check for Dish record
        elif not pd.isna(row[df.columns[2]]) and current_submenu:
            dishes.append({
                'id': int(row[df.columns[2]]),
                'submenu_id': current_submenu['id'],
                'menu_id': current_menu['id'],
                'title': row[df.columns[3]],
                'description': row[df.columns[4]],
                'price': float(row[df.columns[5]])
            })

    return menus, submenus, dishes
