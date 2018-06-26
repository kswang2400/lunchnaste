from menu_data_helpers import (
    CITIES,
    MEALS,
    is_gluten_free,
)

def filter_menu_during_meal(data, meal='Lunch'):
    output = {}
    for key in data:
        if meal in MEALS and meal == key[2]:
            output[key] = data[key]

    return output

def filter_menu_in_buildings(data, buildings=None):
    if not buildings:
        buildings = ['SF']

    output = {}
    for key in data:
        for b in buildings:
            if b in CITIES and b in key[1]:
                output[key] = data[key]

    return output

def format_metadata_for_slack(data):
    output = ''

    for key, value in data.items():
        output += format_building_message(key, value)

    return { 'text': output }

def format_building_message(key, value):
    output = ''

    output += '\n{city} - {building} -- {meal}\n\n'.format(
        city=key[1].split('-')[0],
        building=key[1].split('-')[1].strip('0'),
        meal=key[2]
    )

    for menu_item in value:
        output += format_menu_item_message(menu_item)

    return output

def format_menu_item_message(menu_item):
    return '\t\t{warning}{item}\n'.format(
        warning = '' if is_gluten_free(menu_item['text']) else ':warning: ',
        item=menu_item['text'],
    )
