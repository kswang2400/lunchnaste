CITIES = ('SF', 'CHI', 'NYC', 'SEA',)
MEALS = ('Breakfast', 'Lunch', 'Dinner', 'Back 2 Basics', 'Happy Hour',)

def fix_format_error(data):
    return data.split('-')[-1].strip()

def is_empty(data):
    return ''.join(data.split()) == '' or data == '\u200b'

def is_gluten_free(text):
    if '(' not in text:
        return True

    return 'G' not in text.split('(')[1].split(')')[0]

def menu_section_name(data):
    for meal in MEALS:
        if data.startswith(meal):
            return 'meals'

    for city in CITIES:
        if data.startswith(city):
            return 'city'

    return 'menu_item'

def parse_city_metadata(data):
    for city in CITIES:
        if data.startswith(city):
            return '{city}-{address}'.format(
                city=data[:len(city)],
                address=data[len(city):].zfill(5))

    return False

def parse_meal_metadata(data):
    for meal in MEALS:
        if data.startswith(meal):
            meal = meal.strip()
            theme = data.split('-')[-1].strip()
            return (meal, theme)

    return False
