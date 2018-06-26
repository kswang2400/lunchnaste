CITIES = ('SF', 'CHI', 'NYC', 'SEA',)
MEALS = ('Breakfast', 'Lunch', 'Dinner', 'Back 2 Basics', 'Happy Hour',)


class Allergens:
    def __init__(self, allergens):
        self.is_vegetarian = allergens[0]
        self.is_vegan = allergens[1]
        self.is_gluten_free = allergens[2]
        self.is_made_with_dairy = allergens[3]
        self.is_made_with_nuts = allergens[4]
        self.is_made_with_eggs = allergens[5]
        self.is_made_with_soy = allergens[6]


def fix_format_error(data):
    return data.split('-')[-1].strip()


def is_empty(data):
    return ''.join(data.split()) == '' or data == '\u200b'


def check_allergen_key(text):
    if '(' not in text:
        return Allergens([False]*7)
    allergens = [None]*7
    if text.count('*', text.find('('), text.find(')')) == 3:
        allergens[0], allergens[1] = [True, True]
    elif text.count('*', text.find('('), text.find(')')) == 2:
        allergens[0], allergens[1] = [False, True]
    elif text.count('*', text.find('('), text.find(')')) == 1:
        allergens[0], allergens[1] = [True, False]
    else:
        allergens[0], allergens[1] = [False, False]
    allergens[2] = False if text.count('G', text.find('('), text.find(')')) else True
    allergens[3] = True if text.count('D', text.find('('), text.find(')')) else False
    allergens[4] = True if text.count('N', text.find('('), text.find(')')) else False
    allergens[5] = True if text.count('E', text.find('('), text.find(')')) else False
    allergens[6] = True if text.count('S', text.find('('), text.find(')')) else False
    return Allergens(allergens)


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
